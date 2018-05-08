<?php
$link = mysqli_connect("localhost", "mmcelwai", "123456", "occupancy_data");


if($link === false){

    die("ERROR: Could not connect. " . mysqli_connect_error());

}
if ($_SERVER['REQUEST_METHOD'] === 'POST'){
   $loc = $_POST['locationID'];
   $newAdd = $_POST['macs'];
   if(is_string($newAdd)){
     $newAdd = explode(",",$newAdd);
   } 
   $day = Date("D");
   $hour = Date("H");
   $cur_date = Date("Y-m-d:H");
   $update = 0;
   $count = 0;
   $macAdds = array();
   $insert_data = json_encode($newAdd);
   
   $result = mysqli_query($link,"SELECT id,addr,ttl FROM macAdds WHERE loc = '$loc' and date = '$cur_date'");
   while($row = mysqli_fetch_assoc($result)){
     $ttl = (int)$row['ttl'];
     $id = $row['id'];
     $count = $count +1;
     if($ttl > 0){
      // $macAdds[] = $row['addr'];
       $ttl = $ttl - 1;
       $res = mysqli_query($link, "UPDATE macAdds SET ttl ='$ttl' WHERE id = '$id'");
     }
     else{
       $res = mysqli_query($link, "DELETE FROM macAdds WHERE id = '$id'");

    }
   
   }
   $res = mysqli_query($link, "DELETE FROM macAdds WHERE date != '$cur_date'");

   foreach($newAdd as $addr){
     $newttl = 1;
     
     if(!in_array($addr,$macAdds,TRUE) and !array_search($addr,$macAdds)){
       $macAdds[] = $addr;
       echo $addr . "     " . gettype($addr);
       $result = mysqli_query($link,"INSERT INTO macAdds (loc,date,addr,ttl) VALUES ('$loc','$cur_date','$addr','$newttl')");
       if(!$result){
         echo "ERROR: Not able to execute macadds insertion. " . mysqli_error($link);
       }
     }
     else{
       $result = mysqli_query($link, "UPDATE macAdds SET ttl ='$newttl' WHERE addr = '$addr' ORDER BY id DESC LIMIT 1");

     }
     
   }
   $num_people = count($macAdds);
   $return = mysqli_query($link,"show tables like '$loc'");
   if(mysqli_num_rows($return) == 0){
     $create = mysqli_query($link, "CREATE TABLE $loc (id INT AUTO_INCREMENT,day VARCHAR(20),hour INT, num_people INT,data_count INT NOT NULL,primary key (id))");
     if(!$create){
       echo "create table failed " . mysqli_error($link);
     }

   }

   $data_count = 1;
   $ret_sql="Select num_people,data_count FROM $loc WHERE day = '$day' and hour = '$hour' ORDER BY id DESC LIMIT 1";
   $ret_result = mysqli_query($link, $ret_sql);
   if(mysqli_num_rows($ret_result) > 0){
       $row = mysqli_fetch_assoc($ret_result);
       $old_people = $row['num_people'];
       $data_count = $row['data_count'];
       $update = 1;
       if($old_people){

         $real_time = $num_people;
         $num_people = $old_people*$data_count + $num_people;
         $data_count = $data_count +1;
         $num_people = $num_people / $data_count;
         
       }

   } else{
       echo "ERROR: Could not execute $ret_sql. " . mysqli_error($link);
   }
   if($update){
     $sql = "Update $loc SET num_people = '$num_people',data_count = '$data_count' WHERE
           day = '$day' and hour = '$hour'";
   }
   else{
     $sql = "INSERT INTO $loc (day,hour,num_people,data_count) VALUES
           ('$day','$hour','$num_people','$data_count')";
   }
   if(mysqli_query($link, $sql)){
        //echo "Data added to server";

   } else{
       echo "ERROR: Not able to execute $sql. " . mysqli_error($link);
   }

   $return = mysqli_query($link, "select * from real_time WHERE loc = '$loc'");
   if(mysqli_num_rows($return) > 0){
       if(mysqli_query($link,"UPDATE real_time SET num_people = '$real_time',date = '$cur_date' WHERE loc = '$loc'")){
         //pass
       }
       else{
           echo "ERROR: Not able to update the real time. " . mysqli_error($link);
       }
    } else{
       if(mysqli_query($link,"INSERT into real_time (num_people,date,loc) VALUES ('$num_people','$cur_date','$loc')")){
         //pass
       }
       else{
           echo "ERROR: Not able to update the real time. " . mysqli_error($link);

       }
    }

   
 
   

}


mysqli_close($link);

?>


