% comment
-module(q). % match file name
%-compile(export_all). % warning; bad to export all...
-export([main/0,x1/1,z/0,pn/1,z/1]). % function name / # of params
-import(io,[fwrite/1]).
-record(r,{k,v,d=1.618}).
-define(C,51). % const/macro

% guard sequence
%age(Age) when Age>19 -> adult; % runtime error if actual param range not covered
age(Age) when Age>=13, Age=<19 -> teen; % teen,child,... are 'atoms'
age(Age) when Age>=3, Age<13 -> child;
age(Age) when Age>=1, Age<3 -> toddler.

main() ->
	io:fwrite("howdy~n").

x1(S) ->
%	io:format("~p~n",[s]),
	io:format("~p~n",[S]),
	io:fwrite("howdy~n").

someFunc2() -> % function not exported; internal
	_=0, % anonymous value
	io:fwrite("y\n").
%w(S,V) ->

z(S) ->
	io:fwrite("z/1~p\n",[S]).

% ok to have functions with same names and different # of parameters
z() ->
	io:format("age ~p~n",[age(18)]), % error if no age match
	M1=#{n=>"KRB",z=>true,a=>51}, % map is comma-separated key=>value pairs
	io:format("map ~p~n",[M1]),
	io:format("get ~p~n",[maps:get(n,M1)]),
	Keyname = randomkey,
	case maps:find(Keyname,M1) of
		{ok,Value} ->
			io:format("Found value ~p~n",[Value]); % semi-colon
		error ->
			io:format("No value found for key ~p~n",[Keyname]) % no colon/comma
	end,	
	K="key",V="value",N=51,B=true, 
	io:format("~p~n",[[K,V,N,B]]),
	F = fun() -> true end, % 'fun' is function keyword
	io:format("fun ~p~n",[F()]),
	io:format("multi ~p~n",[17*3]),
	io:format("bool ~p~n",[true]),
	io:format("list ~p~n",[[1,false,1.618,"str"]]), % list is comma-separated in sqare brackets
	io:format("tuple ~p~n",[{"a",3,okie,false,3}]), % tuple is in curly braces
	io:format("str ~p~n",["zxc"]),
	R=#r{k="z",v=51}, % create new record with defaults
	io:format("record ~p~n",[R]),
	io:format("record ~p~n",[[record_info(fields,r),record_info(size,r)]]),
	io:format("C ~p~n",[?C]), % const/macro

	io:fwrite("one\n"),
	io:fwrite("two~n"),

	X = [4,6,8], 
	iterate(X),

	for(3,2),
	for(3,fun(I) -> io:format("~p~n",[I]) end),

	someFunc2().

pn([RemainingLetter|[]]) -> % matches if only one char left, and the 'rest' is empty
	io:format("1~c~n",[RemainingLetter]);
pn([FirstLetter|RestOfName]) -> % matches if string length > 1
	io:format("2~c~n",[FirstLetter]),
	pn(RestOfName).


iterate(L) -> iterate(L,0).
iterate([], Acc) -> Acc;
iterate([I|T], Acc) ->
	io:fwrite("iterate ~w~n",[I]), 
	iterate(T,Acc+1). 
	

for(0,_) -> [];
for(N,Term) when N > 0 ->
%	io:fwrite("for ~w~n",[[N,Term(N)]]), 
	[Term|for(N-1,Term)]. 
