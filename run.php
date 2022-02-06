<?php
header('Content-Type: application/json');
if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    $email = $_POST['email'];
    $pass = $_POST['password'];
    exec("python3 wiregen.py --user $email --pass $pass", $out);
    echo $out[0];
} else {
    die('Method Not Allowed');
}
