#if defined STRLIB_INC
	#endinput
#endif
#define STRLIB_INC

#include <a_samp>

#if !defined STRLIB_RETURN_SIZE
	#define STRLIB_RETURN_SIZE  128
#endif

#if !defined STRLIB_USE_FORMATEX
	#if defined __fmt_funcinc
		#if !defined FormatSpecifier
			#error Please include formatex before strlib.
		#endif
	
		#define STRLIB_USE_FORMATEX  true
	#else
		#define STRLIB_USE_FORMATEX  false
	#endif
#endif

static stock CopyArgumentToHeap(arg, bool:pack = false, const argptr[] = "") {
    new arg_address, address;
    
    #emit LOAD.S.pri  0
    #emit ADD.C       12
    #emit LOAD.S.alt  arg
    #emit SHL.C.alt   2
    #emit ADD
    #emit LOAD.I
    #emit STOR.S.pri  arg_address
    #emit STOR.S.pri  argptr
    
    if (pack) {
        new bytes = ((strlen(argptr) + 1 + 3) / 4) * 4;
        
        #emit LCTRL       2
        #emit STOR.S.pri  address
        #emit LOAD.S.alt  bytes
        #emit ADD
        #emit SCTRL       2
        
        //strpack(dest[], const source[], maxlength = sizeof dest)
        #emit LOAD.S.pri  bytes
        #emit SHR.C.pri   2
        #emit PUSH.pri
        
        #emit PUSH.S      arg_address
        #emit PUSH.S      address
        
        #emit PUSH.C      12
        
        #emit SYSREQ.C    strpack
        #emit STACK       16
    } else {
        new bytes = (strlen(argptr) + 1) * 4;
        
        #emit LCTRL       2
        #emit STOR.S.pri  address
        #emit LOAD.S.alt  bytes
        #emit ADD
        #emit SCTRL       2
        
        //strunpack(dest[], const source[], maxlength = sizeof dest)
        #emit LOAD.S.pri  bytes
        #emit SHR.C.pri   2
        #emit PUSH.pri
        
        #emit PUSH.S      arg_address
        #emit PUSH.S      address
        
        #emit PUSH.C      12
        
        #emit SYSREQ.C    strunpack
        #emit STACK       16
    }
    
    #emit LOAD.S.pri  0
    #emit ADD.C       12
    #emit LOAD.S.alt  arg
    #emit SHL.C.alt   2
    #emit ADD
    #emit MOVE.alt
    #emit LOAD.S.pri  address
    #emit STOR.I
    
    return address;
}

static stock RestoreHeapToAddress(address) {
    #emit LOAD.S.pri  address
    #emit SCTRL       2
}

stock strreplace(string[], const search[], const replacement[], bool:ignorecase = false, pos = 0, limit = -1, maxlength = sizeof(string)) {
    // No need to do anything if the limit is 0.
    if (limit == 0)
        return 0;
    
    new
             sublen = strlen(search),
             replen = strlen(replacement),
        bool:packed = ispacked(string),
             maxlen = maxlength,
             len = strlen(string),
             count = 0
    ;
    
    
    // "maxlen" holds the max string length (not to be confused with "maxlength", which holds the max. array size).
    // Since packed strings hold 4 characters per array slot, we multiply "maxlen" by 4.
    if (packed)
        maxlen *= 4;
    
    // If the length of the substring is 0, we have nothing to look for..
    if (!sublen)
        return 0;
    
    // In this line we both assign the return value from "strfind" to "pos" then check if it's -1.
    while (-1 != (pos = strfind(string, search, ignorecase, pos))) {
        // Delete the string we found
        strdel(string, pos, pos + sublen);
        
        len -= sublen;
        
        // If there's anything to put as replacement, insert it. Make sure there's enough room first.
        if (replen && len + replen < maxlen) {
            strins(string, replacement, pos, maxlength);
            
            pos += replen;
            len += replen;
        }
        
        // Is there a limit of number of replacements, if so, did we break it?
        if (limit != -1 && ++count >= limit)
            break;
    }
    
    return count;
}

stock sprintf(const fmat[], {Float, _}:...) {
    static output[STRLIB_RETURN_SIZE], frm_header[3], heap;
    
    const output_size = sizeof(output);
    
    if (ispacked(fmat)) {
        heap = CopyArgumentToHeap(0);
    } else {
        heap = 0;
    }{}
    
    // Store current frame header
    #emit LCTRL      5
    #emit CONST.alt  frm_header
    #emit MOVS       12
    
    // Change the stack pointer to FRM + 12
    #emit ADD.C    12 // pri is FRM (see above)
    #emit SCTRL    4
    
    // Push sizeof(output)
    #emit PUSH.C      output_size
    
    // Push output
    #emit PUSH.C      output
    
    // Push the argument count
    #emit LOAD.S.pri  8
    #emit ADD.C       8
    #emit PUSH.pri
    
    #if !STRLIB_USE_FORMATEX
        const formatex = 0; // Dummy used to avoid "unknown symbol" error
        
        goto do_sysreq;
    #endif

    // Call formatex (unless this was skipped above)
    #emit LCTRL       6
    #emit ADD.C       36
    #emit PUSH.pri
    #emit CONST.pri   formatex
    #emit SCTRL       6
    
    #if !STRLIB_USE_FORMATEX
        do_sysreq:
    #endif
    
    // Call format (unless formatex was called, in which case this is skipped)
    #emit SYSREQ.C    format
    
    // Restore the stack pointer to FRM
    #emit LCTRL       5
    #emit SCTRL       4
    
    // Copy back the frame header
    #emit MOVE.alt
    #emit CONST.pri   frm_header
    #emit MOVS        12
    
    // Restore heap if needed
    if (heap) {
        RestoreHeapToAddress(heap);
    }{}
    
    // IMPORTANT: Fix compiler bug (returning strings in variadic functions)
    #emit LOAD.S.pri  8
    #emit ADD.C       12
    #emit MOVE.alt
    #emit LCTRL       5
    #emit ADD
    #emit LOAD.I
    #emit STOR.S.pri  20 // 16 + (static_args * 4)
    
    return output;
    
    // It is actually used, just not by its symbol name
    #pragma unused fmat
}

forward bool:isequal(const str1[], const str2[], bool:ignorecase = false);
stock bool:isequal(const str1[], const str2[], bool:ignorecase = false) {
    new
        c1 = (str1[0] > 255) ? str1{0} : str1[0],
        c2 = (str2[0] > 255) ? str2{0} : str2[0]
    ;

    if (!c1 != !c2)
        return false;

    return !strcmp(str1, str2, ignorecase);
}