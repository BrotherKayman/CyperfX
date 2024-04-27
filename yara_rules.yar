rule ExampleMalwareRule1 {
    meta:
        description = "Example malware rule 1"
        author = "Your Name"
        date = "2024-04-23"
    strings:
        $s1 = "malicious_string1" fullword
        $s2 = {6A 40 68 00 30 D4 40} // Example byte sequence
        $s3 = "suspicious_behavior" wide
    condition:
        $s1 or $s2 or $s3
}

rule ExampleMalwareRule2 {
    meta:
        description = "Example malware rule 2"
        author = "Your Name"
        date = "2024-04-23"
    strings:
        $s1 = "malicious_code_signature" fullword
        $s2 = {90 90 90 90 90} // Example NOP sled
        $s3 = "cmd /c echo" wide
    condition:
        $s1 or $s2 or $s3
}

rule ExampleMalwareRule3 {
    meta:
        description = "Example malware rule 3"
        author = "Your Name"
        date = "2024-04-23"
    strings:
        $s1 = "EvilCode" fullword
        $s2 = "C:\\malicious\\file.exe" nocase
        $s3 = "This file contains a virus" nocase wide
    condition:
        $s1 and $s2 and $s3
}
