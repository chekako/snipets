// context
/*
Package context defines the Context type, which carries deadlines, cancellation signals, and other request-scoped values across API boundaries and between processes.
Incoming requests to a server should create a Context, and outgoing calls to servers should accept a Context. The chain of function calls between them must propagate the Context, optionally replacing it with a derived Context created using WithCancel, WithDeadline, WithTimeout, or WithValue.
A Context may be canceled to indicate that work done on its behalf should stop. A Context with a deadline is canceled after the deadline passes. When a Context is canceled, all Contexts derived from it are also canceled.
The WithCancel, WithDeadline, and WithTimeout functions take a Context (the parent) and return a derived Context (the child) and a CancelFunc. Calling the CancelFunc directly cancels the child and its children, removes the parent's reference to the child, and stops any associated timers. Failing to call the CancelFunc leaks the child and its children until the parent is canceled. The go vet tool checks that CancelFuncs are used on all control-flow paths.
*/

/*
WithCancel context allows manually triggered cancellation.
signal.NotifyContext allows cancellation from OS interrupt signal, e.g. SIGTERM, SIGQUIT.
Timeout context allows delay (relative) cancellation.
Deadline context allows absolute date-time cancellation.
*/

/*
WithValue returns a derived context that points to the parent Context. In the derived context, the value associated with key is val.
Use context Values only for request-scoped data that transits processes and APIs, not for passing optional parameters to functions.
The provided key must be comparable and should not be of type string or any other built-in type to avoid collisions between packages using context. Users of WithValue should define their own types for keys. To avoid allocating when assigning to an interface{}, context keys often have concrete type struct{}. Alternatively, exported context key variables' static type should be a pointer or interface.
*/

type favContextKey string

f := func(ctx context.Context, k favContextKey) {
	if v := ctx.Value(k); v != nil {
		fmt.Println("found value:", v)
	} else {
		fmt.Println("key not found:", k)
	}
}

k := favContextKey("language")

ctx0, cancel0 := signal.NotifyContext(context.Background(),
	os.Interrupt, syscall.SIGTERM, syscall.SIGQUIT)
defer cancel0()
ctx1, cancel1 := context.WithTimeout(ctx0, 7*time.Second) // child of ctx0
defer cancel1()
ctx2 := context.WithValue(ctx1, k, "Go") // single key-value pair

f(ctx2, k)
f(ctx2, favContextKey("color"))
