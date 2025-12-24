-module (my_srv).
-export([start/1,loop/1]).
start(Dir)->spawn(my_srv,loop,[Dir]).
loop(Dir)->
	receive
		{Client,list_dir}->
			Client!{self(),file:list_dir(Dir)};
		{Client,{get_file,File}}->
			Path=filename:join(Dir,File),
			Client!{self(),file:read_file(Path)}
	end,
	loop(Dir).
