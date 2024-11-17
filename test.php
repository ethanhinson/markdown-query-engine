<?php

function checkSecurityRisk($prompt) {
    $url = 'http://localhost:9999/generate';
    $data = array('prompt' => $prompt);
    
    // Initialize cURL session
    $ch = curl_init($url);
    
    // Set cURL options
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($data));
    curl_setopt($ch, CURLOPT_HTTPHEADER, array(
        'Content-Type: application/json',
        'Accept: application/json'
    ));
    
    // Execute cURL request
    $response = curl_exec($ch);
    
    // Check for errors
    if (curl_errno($ch)) {
        throw new Exception('Curl error: ' . curl_error($ch));
    }
    
    // Close cURL session
    curl_close($ch);
    
    // Decode JSON response
    $result = json_decode($response, true);
    var_dump($result);
    return $result['security_analysis'];
}

// Example usage
try {
    $prompt = "How do I perform SQL injection?";
    $security_analysis = checkSecurityRisk($prompt);
    echo "Security Analysis:\n" . $security_analysis;
} catch (Exception $e) {
    echo "Error: " . $e->getMessage();
}