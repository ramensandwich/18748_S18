<?php
$link = mysqli_connect("localhost", "mmcelwai", "123456", "occupancy_data");

$day_array = array('Sun','Mon','Tue','Wed','Thu','Fri','Sat');

if ($_SERVER['REQUEST_METHOD'] === 'GET'){
   $req = $_GET['query'];
   $output = array();
//   $sql = "SELECT * FROM $location";
  // $result = mysqli_query($link,$sql);
   $day = date("D");
   $hour = date("H");
   /*while($row=mysqli_fetch_assoc($result))
   {
     $newID = intval($row['id']) - 1;
     $dHour = $row['hour'];
     $dDay = $row['day'];
     $del_sql = "DELETE FROM $location WHERE id = '$newID' and day = '$dDay' and hour = '$dHour'";
     $res = mysqli_query($link,$del_sql);
     if(!$res){
       echo mysqli_error($link);
     }

     
   }*/


   if($req == 'rt'){
     $location = $_GET['locationID'];
     $sql = "SELECT date,num_people FROM real_time WHERE loc = '$location'";
     $result = mysqli_query($link,$sql);
     $row = mysqli_fetch_assoc($result);
     $str_output = "{\"day\"=" . $day .",\"hour\"=" . $hour . ",\"num_people\"=". $row['num_people']. "}";
     $output = json_encode($str_output);
     echo $output;

   }

   else if($req == 'hist'){
     $location = $_GET['locationID'];
     foreach($day_array as $day){
       $hour = 0;
       $output_arr = array();
       while($hour < 24){
        
         $result = mysqli_query($link,"SELECT num_people FROM $location WHERE day = '$day' and hour = '$hour'");
         $assoc = mysqli_fetch_assoc($result);
         $output_arr[] = $assoc['num_people'];

         $hour = $hour+1;
       }
       $output[] = array($day => $output_arr);

     }
     $json_output = $output;
     header('Content-Type: application/json');
     echo json_encode($json_output);
       

    }
    else if($req == "rec"){
      $rec_array = array();
      $day = $_GET['day'];
      $hour = $_GET['hour'];
      $rec_result = mysqli_query($link,"SELECT table_name FROM information_schema.tables");
      while($rec_row = mysqli_fetch_assoc($rec_result)){
        $name = $rec_row['table_name'];
        $name_res = mysqli_query($link,"Select * From real_time where loc = '$name'");
        if((mysqli_num_rows($name_res) > 0) && $name != "test"){
          $result = mysqli_query($link,"SELECT num_people FROM $name where hour = '$hour' and day = '$day'");
          $assoc = mysqli_fetch_assoc($result);
          $rec_array[] = array($name => $assoc['num_people']);
        }    

      }

      echo json_encode($rec_array);

    }


}

mysqli_close($link);

?>


