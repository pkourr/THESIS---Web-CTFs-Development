<?php
// Define the extensions deny list
$ext_denylist = array(
    "php", "php2", "php3", "php4", "php5", "php6", "php7",
    "phps", "pht", "phtm", "phtml", "pgif", "shtml", "phar",
    "inc", "hphp", "ctp"
);

// Specify the maximum file size (in bytes)
$maxFileSize = 5000000; //5MB

// Initialize a variable to store messages
$message = "";

// Check if the form was submitted using POST method
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // Check if file was uploaded without errors
    if (isset($_FILES["fileToUpload"]) && $_FILES["fileToUpload"]["error"] == 0) {
        $filename = $_FILES["fileToUpload"]["name"];
        $filesize = $_FILES["fileToUpload"]["size"];

        // Check if the uploaded file exceeds the maximum size limit
        if ($filesize > $maxFileSize) {
            $message = "<div class='error-msg'>Error: File size is larger than the allowed limit.</div>";
        } else {
            // Extract file extension for further validation
            $ext = pathinfo($filename, PATHINFO_EXTENSION);

            // Check if the file extension is in the deny list
            if (in_array($ext, $ext_denylist)) {
                $message = "<div class='error-msg'><h1>ERROR:</h1> This file type is not allowed.</div>";
            } else {
                // Construct the target filepath where the file will be moved
                $target_file = "/var/www/html/uploads/" . $filename;

                // Attempt to move the uploaded file to the target location
                $moved = move_uploaded_file($_FILES["fileToUpload"]["tmp_name"], $target_file);
                if ($moved) {
                    // Success: File is uploaded. Display success message with link to the file.
                    $message = "<div class='success-msg'><h1>SUCCESS:</h1> Your artwork has been uploaded. View it here: <a href='uploads/$filename'>uploads/$filename</a>.</div>";
                } else {
                    // Failure: File couldn't be moved. Show error message.
                    $message = "<div class='error-msg'><h1>ERROR:</h1> Sorry, there was an error uploading your file '$filename'.<br><br></div>";
                }
            }
        }
    } else {
        // No file selected: Inform the user to choose a file.
        $message = "<div class='error-msg'><h1>ERROR:</h1> No file was selected.</div>";
    }
}
?>


<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no" />
    <title>Digital Art Gallery - Upload</title>
    <link href="https://fonts.googleapis.com/css?family=Open+Sans:700,300" rel="stylesheet">
    <style>@import url(https://fonts.googleapis.com/css?family=Open+Sans:700,300);

        .frame {
            position: absolute;
            top: 50%;
            left: 50%;
            width: 400px;
            height: 400px;
            margin-top: -200px;
            margin-left: -200px;
            border-radius: 2px;
            box-shadow: 4px 8px 16px 0 rgba(0, 0, 0, 0.1);
            overflow: hidden;
            background: linear-gradient(to top right, darkmagenta 0%, hotpink 100%);
            color: #333;
            font-family: "Open Sans", Helvetica, sans-serif;
        }

        .center {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 300px;
            height: 260px;
            border-radius: 3px;
            box-shadow: 8px 10px 15px 0 rgba(0, 0, 0, 0.2);
            background: #fff;
            display: flex;
            align-items: center;
            justify-content: space-evenly;
            flex-direction: column;
        }

        .title {
            width: 100%;
            height: 50px;
            border-bottom: 1px solid #999;
            text-align: center;
        }

        h1 {
            font-size: 16px;
            font-weight: 300;
            color: #666;
        }

        .dropzone {
            width: 100px;
            height: 80px;
            border: 1px dashed #999;
            border-radius: 3px;
            text-align: center;
        }

        .upload-icon {
            margin: 25px 2px 2px 2px;
        }

        .upload-input {
            position: relative;
            top: -62px;
            left: 0;
            width: 100%;
            height: 100%;
            opacity: 0;
        }

        .btn {
            display: block;
            width: 140px;
            height: 40px;
            background: darkmagenta;
            color: #fff;
            border-radius: 3px;
            border: 0;
            box-shadow: 0 3px 0 0 hotpink;
            transition: all 0.3s ease-in-out;
            font-size: 14px;
        }

        .btn:hover {
            background: rebeccapurple;
            box-shadow: 0 3px 0 0 deeppink;
        }

        .success-msg, .error-msg {
            text-align: center;
            margin-top: 20px;
            padding: 10px;
            border-radius: 5px;
        }
        .success-msg {
            color: #4F8A10;
            background-color: #DFF2BF;
        }
        .error-msg {
            color: #D8000C;
            background-color: #FFD2D2;
        }
    </style>
</head>
<body background="pink.jpg">
<nav class="navbar navbar-expand-lg navbar-dark navbar-custom fixed-top">
    <!-- Navigation Content -->
    <a class="navbar-brand" href="index.php">Digital Art Gallery</a>
    <!-- Other navigation elements -->
</nav>

<div class="container mt-5">
    <div class="frame">
        <form method="post" enctype="multipart/form-data">
            <div class="center">
                <div class="title">
                    <h1>Drop file to upload</h1>
                </div>

                <div class="dropzone">
                    <img src="http://100dayscss.com/codepen/upload.svg" class="upload-icon" />
                    <input type="file" class="upload-input" name="fileToUpload" />
                </div>

                <button type="submit" class="btn" name="submit">Upload file</button>
            </div>
        </form>
    </div>
</div>
<!-- Display the message here -->
<?php if (!empty($message)) echo $message; ?>
</body>
</html>