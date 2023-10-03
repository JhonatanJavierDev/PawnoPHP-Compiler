<?php

// Pawn PHP Compiler
// Based on the api created by: https://github.com/sneedman1337

class CodeCompiler {
    private $patterns_output;

    public function __construct() {
        // regex patterns to search for information in the compiler output
        $this->patterns_output = array(
            'header_size' => '/Header size:\s*(\d+)/',
            'code_size' => '/Code size:\s*(\d+)/',
            'data_size' => '/Data size:\s*(\d+)/',
            'stack_size' => '/Stack\/heap size:\s*(\d+)/',
            'total_requirements' => '/Total requirements:\s*(\d+)/',
        );
    }

    public function compileCode($code) {
        try {
            $compiler_path = 'C:/yourpath/build/pawncc.exe'; // compiler path
            $file_name = uniqid() . '.pwn'; // generate a random name for the pawn file
            $project_dir = 'projects'; // projects/code path
            $file_path = $project_dir . '/' . $file_name; // complete path

            if (!file_exists($project_dir)) {
                mkdir($project_dir, 0777, true); 
            }

            // writes in a ".pwn" file the code obtained by a post request
            file_put_contents($file_path, '#pragma option -d3' . PHP_EOL . PHP_EOL . $code);

            
            exec("$compiler_path $file_path 2>&1", $output, $return_code);
            $output = implode(PHP_EOL, $output);

            $this->deleteAmx(); // delete amx files

            $result = array('success' => true, 'complete_output' => $output);

            foreach ($this->patterns_output as $key => $pattern) {
                if (preg_match($pattern, $output, $matches)) {
                    $result[$key] = $matches[1];
                } else {
                    $result[$key] = null;
                }
            }

            return $result;
        } catch (Exception $e) {
            return array('success' => false, 'complete_output' => $e->getMessage());
        }
    }

    public function deleteAmx() {
        $deleted_amx_files = array();

        foreach (glob('*.amx') as $amx_file) {
            try {
                unlink($amx_file);
                $deleted_amx_files[] = $amx_file;
                echo "$amx_file deleted" . PHP_EOL;
            } catch (Exception $e) {
                echo "Error deleting $amx_file: " . $e->getMessage() . PHP_EOL;
            }
        }

        return $deleted_amx_files;
    }
}

// Example usage:
$compiler = new CodeCompiler();
$code = '#include <a_samp>';
$result = $compiler->compileCode($code);

echo "Pawn compiler 3.10.10 Copyright (c) 1997-2006, ITB CompuPhase" . PHP_EOL;
echo "</br>";
echo "Header size: " . $result['header_size'] . " bytes" . PHP_EOL;
echo "</br>";
echo "Code size: " . $result['code_size'] . " bytes" . PHP_EOL;
echo "</br>";
echo "Data size: " . $result['data_size'] . " bytes" . PHP_EOL;
echo "</br>";
echo "Stack/heap size: " . $result['stack_size'] . " bytes; estimated max. usage=" . $result['total_requirements'] . " cells (" . ($result['total_requirements'] * 4) . " bytes)" . PHP_EOL;

?>
