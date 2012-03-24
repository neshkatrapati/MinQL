<?php

//MinQL PHP Methods
//This Library doesnot have
//  1.GTK Support
//  2.Console Inputy
//MinQL Master Symbol Table
$symbols = array();

//MinQL Preprocessing Method
function minql_preprocess($input, $variables = array()) {

    GLOBAL $symbols;
    $chunks = preg_split("/[\s|=#.,]/", $input);

    $count = 0;
    for ($i = 0; $i < count($chunks); $i++) {

        if (strpos($chunks[$i], "&") !== false) {

            if (strpos($input, "&") !== false) {

                if (in_array(substr($chunks[$i], 1), $symbols)) {
                    $t = $symbols[substr($chunks[$i], 1)];
                } else {
                    $t = $variables[$count++];
                }
                $input = str_replace($chunks[$i], $t, $input);

                $symbols[substr($chunks[$i], 1)] = $t;
                //iar = re.split("[\s|=#.,]",input)
            }
        }
    }



    return $input;
}

function minql_show_symbols() {
    GLOBAL $symbols;
    var_dump($symbols);
}

function minql_compile($input, $variables) {
    GLOBAL $symbols;
    $query = "";

    #Checking for redirectable outputs such as * <- abc => demoVar
    $inputArr = preg_split("/=>/", $input);
    $input = trim($inputArr[0], " \n\t");

    #Preprocessing the $query
    $input = minql_preprocess($input, $variables);

    #Initializing output variable 
    if (count($inputArr) > 1) {
        $symbols[trim($inputArr[0], " \t")] = "";
    }


    if (strpos($input, "<-") !== false) {
        $tokens = preg_split("/<-/", $input);
        //Its a Select $query!
        $input = str_replace("^", " DISTINCT ", $input);
        $query = "SELECT " . str_replace("<-", " FROM ", $input);
        if (strpos($input, "|") !== false) {
            $t = explode("|", $input);
            print_r($t);
            $wc = "WHERE " . $t[1];
            $query = $t[0] . " " . $wc;
            $query = "SELECT " . str_replace("<-", " FROM ", $query);
            $query = str_replace("(", " ORDER BY( ", $query);
            $query = str_replace("[", " GROUP BY( ", $query);
            $query = str_replace("]", ")", $query);
        }
    } else if (strpos($input, "->") !== false) {

        $x = str_replace("->", " ", $input);
        $y = preg_split("/->/", $input);

        #Create $query
        if (strpos($y[1], ":") !== false) {
            $qt = "";
            $fields = explode(",", $y[1]);
            for ($j = 0; $j < count($fields); $j++) {
                $fd = explode(":", $fields[$j]);
                $qt .= $fd[0] . " " . $fd[1] . ",";
            }

            $query = "CREATE TABLE " . $y[0] . " (" . substr($qt, 0, -1) . ")";
            #Update $query
        } else if (strpos($input, "=") !== false) {
            $query = "UPDATE " . $y[1] . " SET " . $y[0];
            if (strpos($input, "|") !== false) {
                $t = explode("|", $y[1]);
                $query = "UPDATE " . $t[0] . " SET " . $y[0];
                $wc = " WHERE " . $t[1];
                $query .= $wc;
            }
        } else {

            $query = "INSERT INTO " . $y[1] . " values(" . $y[0] . ")";
        }
    } elseif (strpos($input, "#") !== false) {
        #Delete $query
        $x = explode("#", $input);
        if ($x[1] != "")
            $query = "DELETE FROM " . $x[0] . " WHERE " . $x[1];
        else
            $query = "DELETE FROM " . $x[0];
    }

    return trim($query, " \n\t");
}

function minql_query($query, $connection, $variables = array()) {
    return mysql_query(minql_compile($query, $variables), $connection);
}


?>  