this stack trace

    2013/06/08 14:57:33 Handler crashed with error reflect: Call with too few input arguments
    2013/06/08 14:57:33 /usr/local/Cellar/go/1.1/src/pkg/runtime/panic.c 229
    2013/06/08 14:57:33 /usr/local/Cellar/go/1.1/src/pkg/reflect/value.go 397
    2013/06/08 14:57:33 /usr/local/Cellar/go/1.1/src/pkg/reflect/value.go 345
    2013/06/08 14:57:33 /Users/kevin/code/matasano/src/github.com/hoisie/web/server.go 196
    2013/06/08 14:57:33 /Users/kevin/code/matasano/src/github.com/hoisie/web/server.go 305
    2013/06/08 14:57:33 /Users/kevin/code/matasano/src/github.com/hoisie/web/server.go 87
    2013/06/08 14:57:33 /Users/kevin/code/matasano/src/github.com/hoisie/web/server.go 82
    2013/06/08 14:57:33 /usr/local/Cellar/go/1.1/src/pkg/net/http/server.go 1416
    2013/06/08 14:57:33 /usr/local/Cellar/go/1.1/src/pkg/net/http/server.go 1517
    2013/06/08 14:57:33 /usr/local/Cellar/go/1.1/src/pkg/net/http/server.go 1096
    2013/06/08 14:57:33 /usr/local/Cellar/go/1.1/src/pkg/runtime/proc.c 1223

actually means that the route regex contained too few capture groups, relative
to the function handler
