<?php

set_include_path("./service_spec");

require 'vendor/autoload.php';
include("GPBMetadata/Aigents.php");
include("Aigents/AigentsNewsFeedClient.php");
include("Aigents/Channel.php");
include("Aigents/Feed.php");
include("Aigents/Feeds.php");
include("Aigents/JSONFeed.php");
include("Aigents/Response.php");
include("Aigents/Site.php");
include("Aigents/Topic.php");
include("Aigents/UserInfo.php");

$cl = new Aigents\AigentsNewsFeedClient('localhost:9999',
    ['credentials' => Grpc\ChannelCredentials::createInsecure(),]);

function grpc_response($resp)
{
    if ($resp->code == Grpc\STATUS_OK) {
        echo "Call successful!\n";
        return true;
    }
    else {
        echo "Call NOT successful!\n";
        var_dump($resp);
        return false;
    }
}

function user_login($email, $sec_q, $sec_a)
{
    global $cl;
    echo "Calling UserLogin Service\n";
    $usri = new Aigents\UserInfo();
    $usri->setEmail($email);
    $usri->setSecretQuestion($sec_q);
    $usri->setSecretAnswer($sec_a);
    list($resp, $stat) = $cl->userLogin($usri)->wait();
    if (grpc_response($stat)) {
        $result = $resp->getText();
        echo "Result => Login: $result\n";
    }
}

function fetch_json_feed($channel)
{
    global $cl;
    echo "Calling reqJSON Service\n";
    $chn = new Aigents\Channel();
    $chn->setName($channel);
    list($resp, $stat) = $cl->reqJSON($chn)->wait();
    if (grpc_response($stat)) {
        $result = $resp->getNewsFeed();
        echo "Result => Request JSON: $result\n";
    }
}

function add_topic($label, $pattern)
{
    global $cl;
    echo "Calling addTopic\n";
    $tpc = new Aigents\Topic();
    $tpc->setLabel($label);
    $tpc->setPattern($pattern);
    list($resp, $stat) = $cl->addTopic($tpc)->wait();
    if (grpc_response($stat)) {
        $result = $resp->getText();
        echo "Result => Add Topic: $result\n";
    }
}

function add_sites($site)
{
    global $cl;
    echo "Calling addSite\n";
    $st = new Aigents\Sites();
    $st->setSite($site);
    list($resp, $stat) = $cl->addSite($st)->wait();
    if (grpc_response($stat)) {
        $result = $resp->getText();
        echo "Result => Add Site: $result\n";
    }
}
//user_login("<email>", "<secrect_question>", "<secret_answer>");
fetch_json_feed("satiretech");

?>
