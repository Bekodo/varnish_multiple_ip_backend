backend server1 {
    .host = "IP1";
    .port = "http";
    }

backend server2 {
    .host = "IP2";
    .port = "http";
    }

sub vcl_init {
    new vdir = directors.round_robin();
    vdir.add_backend(server1);
    vdir.add_backend(server2);
}
