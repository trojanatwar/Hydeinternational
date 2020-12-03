<?php

$u_name	=	$_POST['user_name'];
$u_mail	=	$_POST['user_mail'];
$mob_number	=	$_POST['mob_number'];
$u_type	=	$_POST['u_type'];
$u_messege	=	$_POST['messege'];
 
 
$subject		=	"New enquiry";	
$msg 			= 	"<p>Name :".$u_name." </p>";
$msg 		   .= 	"<p>Email :".$u_mail."</p>";       
$msg 		   .= 	"<p>Type :".$mob_number."</p>";       
$msg 		   .=	"<p>Full Name:".$u_type."</p>";
$msg 		   .=	"<p>Messege :".$u_messege."</p>";
 

$to 			=	"rinitajadhav8@gmail.com"; 
$from			=	"shri222pune@gmail.com";
$headers  		= 	"From: $from "."\r\n"; 
$headers 	   .= 	"Content-type: text/html \r\n";

mail($to,$subject,$msg,$headers);
header("Location:index.html");
?>