<?php
// Define an array of IP addresses considered safe (localhost)
$whitelist = array(
    '127.0.0.1',
    '::1'
);

// if this page is accessed from the web server, a special sci-fi title is returned
if(in_array($_SERVER['REMOTE_ADDR'], $whitelist)){
    // Output the contents of the flag.txt file
    echo file_get_contents('/var/www/flag.txt');
    return;
}
// Check if the 'input' GET parameter is provided with the request
if (empty($_GET["input"])) {
    echo "Please include the 'input' GET parameter with your request.";
    return;
}

// Decode the base64-encoded XML input from the GET parameter
$xmlData = base64_decode($_GET["input"]);
// Load the XML and handle errors
$xml = simplexml_load_string($xmlData, null, LIBXML_NOENT) or die("Error parsing XML: "."\n".$xmlData);
// Extract elements from the parsed XML
$firstName = $xml->firstName;
$lastName = $xml->lastName;
$role = $xml->role;

// Generate a random sci-fi character name from a predefined list
$titles = array("Starlord", "Galactic", "Space", "Quantum", "Nebula", "Vortex", "Astro", "Cosmic", "Orbit", "Stellar");
$title = $titles[array_rand($titles)];
// Concatenate the name and title to generate the full sci-fi name
$generatedName = $firstName.' "The '.$title.'" '.$lastName;
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <title>Sci-Fi Character Name Generator</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css">
    <link href="https://fonts.googleapis.com/css?family=Orbitron:400,700" rel="stylesheet">
    <style type="text/css">
        body {
            background-image: url("sci-fi-background.jpg");
            background-color: #000000;
            background-size: cover;
            font-family: 'Orbitron', sans-serif;
            margin: 0;
            padding: 0;
            height: 100vh;
        }
        .jumbotron {
            background: rgba(0, 0, 0, 0.8);
            color: #fff;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0,0,0,0.5);
            padding: 40px;
            margin-top: 100px;
        }
        h1, h2 {
            text-align: center;
            margin-bottom: 30px;
        }
        a {
            color: #5603ad;
            font-weight: bold;
            text-decoration: none;
        }
        a:hover {
            color: #682db7;
            text-decoration: underline;
        }
        .container {
            width: 100%; /* Full width to center the content in the viewport */
            display: flex; /* Use flexbox for centering */
            justify-content: center; /* Center horizontally */
            align-items: center; /* Center vertically */
            height: 100vh; /* Full height to center vertically */
        }
    </style>
</head>

<body>

<div class="container">
    <div class="jumbotron">
        <h1>Your Sci-Fi Character Name Is:</h1>
        <h2><?= htmlspecialchars($generatedName, ENT_QUOTES, 'UTF-8') ?></h2>
        <!-- Special sci-fi Character Name functionality: To test the special sci-fi title functionality, make sure you're accessing this page from the web server. -->
        <a href="index.html">Go Back</a>
    </div>
</div>

</body>
</html>
