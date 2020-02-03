<?php

$cl = new Tutorial\ServiceDefinitionClient('localhost:7070', ['credentials' => Grpc\ChannelCredentials::createInsecure(),]);

function do_div()
{
    global $cl;
    echo "<p>Calling Div Service</p>";
    $ipair = new Tutorial\IntPair();
    $ipair.setA(12);
    $ipair.setB(4);
    list($sint, $stat) = $cl->div($ipair)->wait();
    echo "<p>Result => $sint->getV() </p>";
}

do_div();

?>
