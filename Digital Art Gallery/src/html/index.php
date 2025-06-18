<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Explore and share digital art in our unique gallery.">
    <title>Digital Art Gallery</title>
    <style>
        body {
            font-family: 'Arial', sans-serif;
            margin: 0;
            padding: 0;
            background-image: url('art_background.jpg');
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
            color: #fff; /* Assuming a light-colored background image */
            text-align: center;
        }
        .header {
            padding: 40px 0;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.6); /* To make text stand out */
        }
        .header h1 {
            margin: 0;
            font-size: 3em;
        }
        .header p {
            font-size: 1.2em;
            margin-top: 10px;
        }
        .main-content {
            background-color: rgba(0, 0, 0, 0.6); /* Semi-transparent dark overlay for readability */
            padding: 20px;
            margin: 30px auto;
            width: 80%;
            max-width: 600px;
            border-radius: 8px;
            box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);
        }
        .upload-btn {
            background-color: #e67300; /* A bright, attractive color */
            color: white;
            padding: 12px 24px;
            text-decoration: none;
            display: inline-block;
            margin: 20px 0;
            border-radius: 5px;
            transition: background-color 0.3s, transform 0.3s;
            border: none; /* No border */
            font-size: 1em;
        }
        .upload-btn:hover {
            background-color: #ff8000;
            transform: translateY(-2px);
            cursor: pointer;
        }
        footer {
            color: white;
            padding: 20px 0;
            position: relative;
            width: 100%;
            margin-top: 30px;
            text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.5);
        }
    </style>
</head>
<body>
<div class="header">
    <h1>Welcome to the Digital Art Gallery</h1>
    <p>Discover and share amazing digital artworks</p>
</div>

<div class="main-content">
    <h2>Explore the Beauty of Digital Art</h2>
    <p>Join our community of artists and art enthusiasts. View the gallery or share your own masterpieces.</p>
    <a href="upload_art.php" class="upload-btn">Upload Your Art</a>
</div>

<footer>
    <p>Digital Art Gallery © 2023. All Rights Reserved.</p>
</footer>
</body>
</html>
