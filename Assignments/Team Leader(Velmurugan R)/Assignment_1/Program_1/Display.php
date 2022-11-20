<html>
    <head>
        <style>
            body {
                background-color: White;
                font-family: Times New Roman;
                font-size: 25px;
            }
            p {
                font-weight: bold;
                color: Black;
            }
        </style>
    </head>
    <body>
        <h1>USER DETAILS:</h1>
        <p>USER NAME:</p><?php echo $_POST["uname"]; ?><br>
        <p>EMAIL ID:</p><?php echo $_POST["mail"]; ?><br>
        <p>PHONE NUMBER:</p><?php echo $_POST["ph"]; ?><br>
    </body>
</html>