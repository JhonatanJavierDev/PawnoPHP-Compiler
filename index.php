<?php

class CodeCompiler {
    private $patternsOutput;

    const COMPILER_PATH = 'C:/yourpath/build/pawncc.exe';
    const PROJECT_DIR = 'projects';

    public function __construct() {
        $this->patternsOutput = [
            'header_size' => '/Header size:\s*(\d+)/',
            'code_size' => '/Code size:\s*(\d+)/',
            'data_size' => '/Data size:\s*(\d+)/',
            'stack_size' => '/Stack\/heap size:\s*(\d+)/',
            'total_requirements' => '/Total requirements:\s*(\d+)/',
        ];
    }

    public function compileCode($code) {
        try {
            $fileName = uniqid() . '.pwn';
            $filePath = self::PROJECT_DIR . '/' . $fileName;

            if (!file_exists(self::PROJECT_DIR)) {
                mkdir(self::PROJECT_DIR, 0777, true); 
            }

            file_put_contents($filePath, '#pragma option -d3' . PHP_EOL . PHP_EOL . $code);

            exec(self::COMPILER_PATH . " $filePath 2>&1", $output, $returnCode);
            $output = implode(PHP_EOL, $output);

            $this->deleteAmx();

            $result = ['success' => true, 'complete_output' => $output];

            foreach ($this->patternsOutput as $key => $pattern) {
                $result[$key] = preg_match($pattern, $output, $matches) ? $matches[1] : null;
            }

            return $result;
        } catch (Exception $e) {
            return ['success' => false, 'complete_output' => $e->getMessage()];
        }
    }

    public function deleteAmx() {
        $deletedAmxFiles = [];

        foreach (glob('*.amx') as $amxFile) {
            try {
                unlink($amxFile);
                $deletedAmxFiles[] = $amxFile;
                echo "$amxFile deleted" . PHP_EOL;
            } catch (Exception $e) {
                echo "Error deleting $amxFile: " . $e->getMessage() . PHP_EOL;
            }
        }

        return $deletedAmxFiles;
    }
}

$compiler = new CodeCompiler();
$code = '#include <a_samp>';
$result = $compiler->compileCode($code);

echo "Pawn compiler 3.10.10 Copyright (c) 1997-2006, ITB CompuPhase\n";
echo "Header size: " . $result['header_size'] . " bytes\n";
echo "Code size: " . $result['code_size'] . " bytes\n";
echo "Data size: " . $result['data_size'] . " bytes\n";
echo "Stack/heap size: " . $result['stack_size'] . " bytes; estimated max. usage=" . $result['total_requirements'] . " cells (" . ($result['total_requirements'] * 4) . " bytes)\n";
