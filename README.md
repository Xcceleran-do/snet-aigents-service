# Aigents SNET Service

[Aigents](https://aigents.com) is a news monitoring engine. It crawls trusted
sites looking for topics of interest and also supports social media integration
for social relevance of news articles. The main engine can be found on
[Github](https://github.com/aigents/aigents-java) and it offers an http API for
interaction. The [aigents.com](aigents.com) website is an application with a GUI
that makes it easy to use the Aigents engine.

Users can create accounts using an email address, a secret question and answer
which are used for logging in. Each account can have its own list of topics of
interest, trusted list of sites and social media integration. Based on these,
the engine will crawl trusted sites looking for users' topics, correlate news
with what friends are sharing and provide the user with a list of news articles
from thirdparty sites in various formats.

This repo contains a minimalistic SingularityNET service wrapper for the aigents
engine deployed at https://aigents.icog-labs.com to serve as one of the
componenents for delivering news to the [Xccelerando](xcceleran.do) website.


## Service

The service is preferred to run in a container for which a
[Dockerfile](./Dockerfile) is provided here. There's also a script which can
take care of building the image, creating the container (launching the service)
and building the protobufs.

The manage script has the following options
    ```
    Usage: bash manage.sh OPTION [LABEL] [SERVICE_PORT]
      Options:
        build        build the docker image
        run          run the snet service (start container)
        stop         stop the snet service (stop container)
        build-proto  build the proto files

      LABEL  :  image and container label (optional - default=date)

      SERVICE_PORT  :  port to expose the service through (optional - default=9999)
    ```

If no label is provided during build and run, the script will create a docker
image and container named `snet_aigents` with the day's month and day as the tag.
The `build-proto` option is mainly for development. It builds the aigents.proto
file for Python and PHP and keep them in [service_spec](./service_spec)

## Client

There are example client codes for both Python and PHP. The PHP is chosen for
integration as a Wordpress plugin (Option 2 of XND design)

It's best if the PHP client runs outside a container because usually webservers
are of a limited capacity and running a container might not be very ideal. If
one wantes to go through running the PHP GRPC client directly then the follwing
instruction will be useful for setting PHP GRPC up.

### Installing PHP GRPC

This instruction assumes the reader is using Ubuntu 18.04 with PHP 7.2

Let's begin by installing PHP 7.2 (the following commands require sudo)
```
    apt-get update
    apt-get install php7.2
```

We need phpize and php-pear for PHP extension management.
(the following commands require sudo)
```
    apt-get install php7.2-dev php-pear
```
Then using the `pecl` command we install protobuf and grpc
(the following commands require sudo)
```
    pecl install protobuf
    pecl install grpc
```

Once the above two commands have sucessfuly installed protobuf and grpc, we need
to let PHP know to load those extensions.
First create two files in `/etc/php/7.2/mods-available` named `grpc.ini` and
`protobuf.ini` with each containing the following lines respectively:
grpc.ini:
```
    extension=grpc.so
```
protobuf.ini
```
    extension=protobuf.so
```

Once this is done, we need to enable the modules so that they can be used by
PHP. In order to do that, we can use the command `phpenmod` as:
```
    phpenmod protobuf
    phpenmod grpc
```

To make sure that it's successfully installed and working you can run:
```
    php -i | grep grpc
```
If everything went well, you will see something that contains:
```
    grpc support => enabled
    grpc module version => 1.26.0
```

Now you can use the [test_get_json_news.php](./test_get_json_news.php)





For questions and comments:
Dagim Sisay <dagim@singularitynet.io>
