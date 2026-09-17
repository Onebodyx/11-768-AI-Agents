# CMU AI Agents 2026: 2. Tool Use for Language Model Agents

- Видео: https://www.youtube.com/watch?v=jXChFB4JSyw
- Длительность: 57:22
- Дата публикации: 20260908

## Расшифровка

[00:04] Okay. So, hi everyone. Uh, welcome to
[00:07] class number two. Today,
[00:09] uh, today I'll be talking about tool use
[00:13] for language model agents. And, uh, this
[00:15] is, you know, the the most fundamental
[00:17] thing about agents that, uh, you know,
[00:19] makes them different from a language
[00:27] Um so the basic idea here is uh that
[00:29] we're going to be um a tool is basically
[00:31] an interface through which a language
[00:33] model can invoke an external computer
[00:38] program. And uh this is a language model
[00:40] cannot do this on its own because it's
[00:42] fundamentally a token predicting
[00:46] machine. But this enables you to do you
[00:48] know many many different things. So you
[00:49] know you can search, you can call a
[00:52] calculator, you can call a browser, um
[00:53] you can call Python, you can call
[00:57] arbitrary APIs and so uh the language
[01:01] model kind of as you'll see the method
[01:04] for tool calling is standardized but
[01:06] what you do downstream with the tool
[01:09] call can be very different.
[01:12] So there's basically two uh benefits of
[01:15] tools and all of this is from one of the
[01:17] readings that I I posted on the website
[01:18] if you want to go back and read more
[01:22] about it. Uh this is a survey that uh I
[01:25] we wrote uh together Daniel and I and
[01:27] Zoro Wong, one of our our students. Um
[01:31] and the first thing is extending the
[01:33] ability of language models. So this is
[01:35] giving language models the ability to do
[01:37] something that they fundamentally cannot
[01:40] do. And so this could be like accessing
[01:41] information or actions that are outside
[01:45] the language model's um you know action
[01:47] space. The second thing is uh
[01:49] facilitating the language model. And so
[01:51] what I mean by this is this is something
[01:53] that fundamentally the language model
[01:58] can do but it's just a lot easier if you
[01:59] don't if you don't require the language
[02:02] model to do it.
[02:05] So um can anybody come up with an
[02:08] example or well I guess we already have
[02:10] an example in here. So like one thing
[02:11] the the language model fundamentally
[02:14] cannot do would be get the time four
[02:15] months ago or something like that. So
[02:18] the most recent information it saw is uh
[02:20] from four months ago and then its
[02:22] parameters are frozen. So there's no way
[02:24] it could know that without calling you
[02:26] know an external function. On the other
[02:28] hand, uh something in the realm of
[02:31] facilitating is language models can do
[02:34] math actually quite well nowadays, but
[02:36] they take a lot longer than calling a
[02:38] calculator to do math because they have
[02:40] to do reasoning like you ask them to
[02:43] multiply uh two seven-digit numbers and
[02:45] it will take them a very long time to do
[02:46] it where a calculator can do that really
[02:49] quickly. So those are the two kind of
[02:52] basic categories.
[02:54] So um to go a little bit more deeply
[02:57] into those uh you can do things like
[02:59] look up current information um and the
[03:01] benefit of this is this gives you you
[03:04] know fresh evidence to uh ground your
[03:07] answers uh do exact computation using
[03:09] like calculators or python this gives
[03:12] you the ability to execute more reliably
[03:13] or and quickly than using the language
[03:15] model itself.
[03:18] Um other things is uh access private
[03:20] states. So giving the model access to
[03:22] like information about the user so they
[03:25] can uh respond based on the user state
[03:27] um or uh make a change to your external
[03:28] environment. So this could be like
[03:37] So to have some examples of these um if
[03:39] we think about chat GPT
[03:43] uh chat GPT used to like literally just
[03:45] be text in and text out when it first
[03:48] came out. it, you know, the the only
[03:49] thing that it could do was give you
[03:52] textual responses to uh your queries.
[03:54] Now, it's kind of an everything app. It
[03:55] allows you to do so many different
[03:58] things. Um,
[04:00] so like what what are some of the
[04:05] examples of things that uh you know are
[04:08] your top use cases of uh of using chat
[04:10] GPD now?
[04:11] >> Yeah.
[04:15] >> Writing code. Okay. So uh what what tool
[04:18] would you need for something like that?
[04:21] uh like cursor or codeex I think they
[04:23] they can invoke like
[04:25] >> okay but that's not chat GPT right
[04:27] that's cursor or codeex yeah I mean chat
[04:30] GPT like in the chat GPT interface
[04:32] >> they can use blender so they they can
[04:36] render blender okay things so that
[04:39] that's an example of um something that
[04:41] requires executing code but also like
[04:43] displaying it in the appropriate format
[04:46] um any any other ones that people do
[04:49] yeah Just the web page generate images.
[04:51] >> Generate images. Yeah. So that that's
[04:54] calling an image generation tool. Any
[04:56] others?
[05:08] Yeah. So recommend products like a
[05:10] blender or something like this. And for
[05:12] this uh what what sort of tool do you
[05:14] think it would need?
[05:16] >> Some sort of like web searches like
[05:19] Google or Amazon to find.
[05:21] >> Yep. So you might need like arbitrary
[05:23] web search or you might need an API that
[05:25] directly links into Google or Amazon or
[05:27] something like that. Yeah. Any other
[05:29] like weirder weirder ones? Things you
[05:31] were surprised chat GPT was able to do?
[05:31] >> Yeah.
[05:35] >> You can render latex quite nicely.
[05:38] >> Okay. messed up files when I fix you the
[05:39] PDF
[05:41] >> and compile everything which is very
[05:42] handy sometimes.
[05:44] >> Yep. Ren, it can render latex. Well, I
[05:46] actually don't know if this is a tool or
[05:48] if this is just a front-end interface
[05:50] thing, but it might be just that it's
[05:52] rendered in your web browser.
[05:54] >> Oh, it creates a PDF. So, okay. Is a
[05:57] tool. Okay. Very cool. Yeah.
[05:59] >> Interact
[06:01] >> uh interact with like Slack or something
[06:02] like that. So, that's another
[06:04] specialized API. So all kinds of
[06:07] different things. Um I I kind of
[06:09] categorized these into a list of things
[06:12] that I think are um the most uh like
[06:15] typical tools and most of the other
[06:17] tools can kind of be categorized into
[06:19] each of these. So the first one is uh
[06:22] textual responses. So this is kind of
[06:23] the boring one where it just gives you
[06:27] an answer. Um there's two ways you can
[06:30] implement this within an agentic uh like
[06:33] loop. By the way, chat GPT is is an
[06:35] agent now. Uh if you're like if there
[06:37] was any question about it, chat GPD is
[06:38] not just a chat app. It's an agent
[06:41] because it makes uh iterative tool calls
[06:42] to answer your queries. So that's kind
[06:46] of the definition of an agent. Um but uh
[06:47] textual responses, there's two ways you
[06:49] can implement these. One way you can
[06:53] implement these is you can have a finish
[06:55] tool that says, "Okay, I'm done
[06:56] interacting with the user, so I'm just
[06:58] going to finish and and output some
[07:00] text." The other way you can do it is if
[07:02] the agent decides to not call a tool,
[07:04] you can just finish the agentic loop. So
[07:06] that's kind of uh you know the the
[07:11] simple u you know most obvious one.
[07:15] Another extremely common one. Um so all
[07:16] all of these are tools and so like
[07:18] theoretically all of them can be thought
[07:20] of as an API but uh just to break them
[07:23] down a little bit more. Um another one
[07:25] is searching the web and this is you
[07:28] know pulling in information um from all
[07:32] of these uh different settings. Um how
[07:34] many people have heard of retrieval
[07:36] augmented generation? Probably everybody
[07:39] everybody who took the NLP class here uh
[07:41] you know has heard of it but a lot of
[07:43] people. How many people have heard like
[07:46] rag is dead?
[07:47] [snorts and laughter] A fairly large
[07:49] number of people. So there there's been
[07:50] an argument in like language model
[07:52] circles that retrieval augmented
[07:54] generation was so like two years ago and
[07:56] like nobody cares about it anymore. My
[07:59] argument here is a retrieval augmented
[08:00] generation where you retrieve context
[08:02] and then generate answers based on it
[08:04] has become so normal that people don't
[08:06] even realize that they're using it
[08:09] anymore. And so um it's it's so alive
[08:12] that people think it's dead. Um but uh
[08:14] basically you know searching the web and
[08:16] retrieving information and then
[08:18] generating answers based on it is now
[08:21] essentially the norm uh within these uh
[08:23] these applications. Now so uh that's
[08:25] another tool that's provided very very
[08:29] broadly and like any chat uh interface.
[08:32] Another one is code execution and so
[08:35] this is uh throwing in uh you know a set
[08:38] of code to do uh calculations or or
[08:40] something like this. very useful for uh
[08:42] computation all the other stuff we
[08:45] talked about. Another common one is uh
[08:49] having some sort of image generation and
[08:51] uh this this is you know obviously
[08:53] another very popular use case in chat
[08:56] GPT. Um this one's a little bit
[08:57] different because like all of the other
[08:59] ones here uh that I was talking about
[09:02] basically you know mostly interface with
[09:06] text. Um here this is interfacing with
[09:09] uh this is interfacing with images. One
[09:12] interesting thing is uh you'll notice
[09:16] that this is not the same thing is here.
[09:19] So this is like water watercolor robot
[09:21] studying in a library where the query
[09:25] was actually different. And so a big
[09:27] part of calling these images is actually
[09:29] deciding what query to put in there. So
[09:31] the language model will like really
[09:33] really expand the query before it calls
[09:35] an image generation API. I don't know if
[09:37] you can see this anymore in chat GPT,
[09:38] but you used to be able to see in chat
[09:41] GPT when you downloaded the image um
[09:42] that it would have like a very different
[09:44] caption than the caption you gave and
[09:46] you could kind of like latently see what
[09:48] the uh what query the the image
[09:50] generator uh sent to the generate image
[09:53] tool.
[09:56] Then there's all all kinds of uh you
[10:00] know custom functions. So, um, like buy
[10:03] me buy me bananas, uh, milk and coffee.
[10:05] Um, so, you know, this could create a
[10:08] grocery cart, uh, for you and call the
[10:12] like Instacart API to do this. Um, and
[10:13] you can basically go as wild as you want
[10:15] with all these tools and and add
[10:24] Okay, so there's a bunch of different
[10:27] ways you can think about tool calling.
[10:28] Um the first way you can think about
[10:32] tool calling is just
[10:37] you provide a list of uh 50 or 70 API
[10:39] functions that the agent is able to
[10:42] inter interact with and it can call
[10:45] these uh APIs and if you do that
[10:47] basically what you're doing is like
[10:49] every step you're calling one API or if
[10:50] you're doing parallel tool calling
[10:51] you're calling multiple APIs or
[10:55] something like this but code is kind of
[11:00] a special uh API uh because code is
[11:01] extremely
[11:04] uh you know expressive and you can view
[11:08] code as like a meta tool right so within
[11:10] this we have like the bakers baked 200
[11:11] loaves of bread how many loaves of bread
[11:14] did they have left here this is calling
[11:17] an assignment tool an assignment tool
[11:20] this is calling a subtraction tool um
[11:23] this is calling a uh assignment tool you
[11:27] know etc etc so like essentially
[11:29] Um I I imagine that a lot of people have
[11:30] taken like a programming languages
[11:33] course or have some familiar familiarity
[11:35] with programming languages but basically
[11:38] you you can express
[11:41] each piece of code is a tree of these
[11:44] function calls um and these uh the tree
[11:47] can also be have loops and other uh
[11:49] control flow in it. So it's essentially
[11:52] you know a very rich way of calling uh
[11:56] tools. Um and so uh you can also pull in
[11:59] external libraries. So these are now the
[12:02] custom APIs that you pull into your uh
[12:05] pull into your system. So uh you know
[12:07] now if you're calling pandas now you've
[12:10] opened up all of the like tools in
[12:12] pandas right
[12:16] and um you know you can build your own
[12:20] utility functions. So you could call uh
[12:22] special purpose functions that you want
[12:25] uh as well. So
[12:27] code is kind of special. It's like one
[12:29] of the one of the you know special
[12:33] things that uh it's different from other
[12:35] tools in the way that it like opens up
[12:37] your ability to call tools in new ways.
[12:39] And so there's actually uh research work
[12:41] that demonstrates that this is very
[12:44] effective. Uh right now we basically
[12:46] take it for granted but this was not how
[12:49] uh not how we called tools like three or
[12:52] four years ago uh when we first started
[12:55] uh you know building agents with LLMs.
[12:58] And so the the standard then was like if
[13:00] you got a a query sorry this is very
[13:02] small but um it basically says determine
[13:04] the most cost-effective country to
[13:07] purchase the smartphone model Kodak 1.
[13:09] Uh the countries to consider are the US
[13:12] uh Japan, Germany and India. Basically,
[13:16] what this would require you to do was uh
[13:18] you would call your lookup rates tool on
[13:20] Germany. Um you would call your lookup
[13:23] phone price uh tool. You would call uh
[13:26] convert and tax. Then you would call
[13:28] lookup rates again. Then you would call
[13:30] uh look up phone price and you would
[13:32] step over and over and over again uh in
[13:35] order to uh finally get uh finally get
[13:37] the result.
[13:39] But if you write code, you can just
[13:41] write like a single program to perform
[13:43] this. And so uh this makes it like a
[13:46] much richer uh a much more efficient way
[13:48] of calling tools in addition to be being
[13:51] richer. And so this method called uh
[13:55] called Kodak has a paper uh about it and
[13:56] uh some of the core results from the
[13:58] paper are essentially the success rate
[14:00] goes up and the average number of
[14:03] interaction turns goes down. And this is
[14:06] even for tasks that didn't traditionally
[14:08] require code. These are for tasks that
[14:10] were like viewed as regular tool use
[14:13] tasks. Um but like code is just like a
[14:15] good medium uh for how you would do
[14:18] this.
[14:20] Um but there's a reason why people don't
[14:22] use code uh programmatic tool calling
[14:25] for everything. Um and it largely has to
[14:29] do with um with like the level of power
[14:31] that you want to give to the agent. So
[14:33] code is very highowered. So it's
[14:36] expressive. It gives you loop variables
[14:38] and libraries. This is good. But what
[14:41] could be a downside of this?
[14:44] Any ideas? Ju just with respect to loops
[14:46] variables uh loops and variables at
[14:48] first maybe. Yeah.
[14:49] >> Get stuck.
[14:50] >> Yeah, it could get stuck. So it could
[14:52] write an infinite loop and then you need
[14:53] to have something in your system to deal
[14:56] with infinite loops, right? That's uh
[14:58] that's a little bit annoying. Um what
[15:01] about libraries?
[15:03] any problem with that?
[15:05] >> Yeah, security problems would be one
[15:07] thing. Also, maybe just versioning and
[15:09] stuff like this, but um I'm not sure if
[15:11] people are familiar with this, but one
[15:13] of the major issues with agents in cyber
[15:15] security right now is the agents will
[15:17] pull in a library that has been
[15:20] compromised. Um the agent gets
[15:21] compromised and then your whole system
[15:23] gets compromised. So, uh this is
[15:25] something uh something you need to be
[15:27] very careful about.
[15:30] Um they're also uh harder con to
[15:31] constrain because they have the broad
[15:34] action space. So uh it's you know harder
[15:36] to validate and uh get predictable
[15:38] behavior. Um they also have higher
[15:40] impact. So they can you know use more
[15:43] disk uh sorry use more memory, use more
[15:45] disk, use more CPU and stuff like this.
[15:47] And so because of this um we'll talk
[15:48] about this more in the safety lecture,
[15:51] but like once you move to programmatic
[15:53] tool calling, you need to be uh you need
[15:55] to think about sandboxes and how you're
[15:56] going to contain the agent and stuff
[15:59] like that as well.
[16:09] Cool.
[16:12] Okay. So I want to uh talk next about
[16:14] the mech uh mechanics of providing tools
[16:19] and right now uh every language model is
[16:22] basically pretty good at uh like calling
[16:24] tools but this was not you know taken
[16:26] for granted. I I think I mentioned this
[16:28] on Tuesday as well. Um but basically
[16:32] tool calls are um expressed as tokens
[16:35] like this. And so um you know a text
[16:39] continuation is the weather is sunny. A
[16:43] tool continuation is uh like a tool call
[16:44] and then you have get weather or
[16:46] something like this within the the tool
[16:50] call. And very often uh you have both in
[16:53] the same uh output. So if you remember
[16:57] react uh which was talked about before
[17:03] um I can actually draw this on the board
[17:06] but react basically you have your text
[17:08] up here
[17:12] and then you have your uh tool call
[17:14] and then you have your tool call down
[17:21] Yeah, this is like the end of the tool
[17:24] call.
[17:27] And so now you have the the model be
[17:31] being uh giving a response to the human
[17:33] uh while it's making the tool call. And
[17:35] then uh in here you have the like actual
[17:37] tool call that it's making. And so the
[17:39] react loop is no longer expressed as
[17:42] like separate code. It's expressed more
[17:45] as like just a single completion. um if
[17:49] you're using one of the reasoning models
[17:50] um
[17:53] that can reason uh like have long
[17:56] reasoning traces and stuff like that. In
[17:57] addition, you might have like the
[17:59] thinking tokens up here and then a
[18:02] message and then the tool calls. And so
[18:03] the thinking is like very verbose
[18:05] thinking that you don't show to the
[18:07] user. The text is the less verbose uh
[18:09] message that you show to the user and
[18:11] then the tool call is like the actual
[18:14] output you have there.
[18:15] Yeah,
[18:17] >> the tool call tokens has to be in the
[18:19] vocabulary of the model during
[18:21] pre-training also, right?
[18:21] >> Yes.
[18:23] >> So all of these service tokens are going
[18:26] to be vocabulary.
[18:29] >> Uh yes. So actually that's a good point.
[18:31] I said yes, but the answer might be no.
[18:32] I'm going to repeat the question first.
[18:35] So the question was um do these tokens
[18:36] have to be in the vocabulary when you do
[18:39] pre-training? Um, typically if you're
[18:41] pre-training on all of the internet, you
[18:43] don't necessarily have to have them in
[18:47] the vocabulary yet. Um we there are
[18:49] cases where you might do that but it's
[18:51] actually more typical to introduce them
[18:53] in a process of mid-training which is
[18:56] like uh between uh it's when you're
[18:59] training on like moderately large
[19:01] amounts of data on things in the format
[19:03] that you like and then uh you might do
[19:05] reinforcement learning after that but
[19:06] you might not necessarily have them when
[19:10] you pre-train on the whole internet.
[19:13] Cool. Um
[19:15] so
[19:19] I think this should likely be familiar
[19:22] to um you know uh people who have
[19:24] implemented things in uh previous
[19:26] natural language processing or or
[19:29] whatever courses. But um if you have the
[19:31] chat format like the open AAI chat
[19:33] format you have things like the system
[19:35] message, the user message, the assistant
[19:37] message and then uh these are
[19:42] represented as something like JSON in
[19:44] uh like in Python when you call the call
[19:48] the model but these get converted into
[19:50] something uh with like a special token
[19:54] here the system uh like this is a system
[19:56] prompt and then be concise and stuff
[19:59] like this. So like each chat message
[20:01] gets its own format and this is an
[20:04] example of the quen format
[20:07] but uh as I'll show later the other uh
[20:08] other functions are in different
[20:11] formats. So
[20:15] tools basically um add a structure to
[20:16] the request and so you have a tool
[20:19] definition like this and uh this tells
[20:22] you that it's a function. The function
[20:24] name might be get weather. Um the
[20:28] parameters are city and the type is a
[20:33] string and this is required. And this
[20:35] schema gets passed to for example the
[20:37] chat completions function that you you
[20:39] would use when calling openAI or
[20:47] So um when the prompt uh contains
[20:49] something like this, you might have uh
[20:51] this included in the tools section of
[20:54] the prompt and then the output uh ends
[20:57] up being something like name get weather
[20:58] uh with the appropriate arguments like
[21:05] So um we we had a question about how you
[21:08] pre-train the models and um you might
[21:10] not be pre-training but at least at
[21:12] mid-training and beyond you will be
[21:13] training the model to fit a particular
[21:15] tool call format. The interesting thing
[21:17] is uh every model has a different tool
[21:20] call format. Maybe not everyone but many
[21:24] of the different ones. And so uh Quen
[21:29] has like im start tool call uh IM end.
[21:32] Uh Mistall has tool calls and then uh
[21:34] all of the tool calls. Deepseek has
[21:37] their like DSML DeepS markup language
[21:39] function calls. They they don't call it
[21:41] tool calls. they call it function calls
[21:44] and then evoke invoke and basically you
[21:46] know any of these works. Um there might
[21:49] be like minor minor differences in uh
[21:50] which one gets better performance or not
[21:52] if you train the same model with the
[21:54] same data. Uh but
[21:56] what you need to know is you need to
[21:57] know that these are different. So you
[21:59] can't just assume that like some parsing
[22:01] code that works with deepseek will
[22:03] suddenly work with quen and vice versa.
[22:04] Yeah.
[22:09] >> You said you add functionality.
[22:19] >> Um, so what do you mean by loose
[22:38] >> Yep. fine tuning
[22:39] set of
[22:41] >> Yeah. So when you're when you're
[22:44] fine-tuning, you will want to match like
[22:46] if you're fine-tuning
[22:48] from a model that's already been
[22:50] trained, you 100% want to match the tool
[22:51] call format. You don't want to try to
[22:53] get it to do something it wasn't trained
[22:57] on. Um, and the good news is this is all
[22:59] implemented in like hugging face with
[23:02] the apply chat template uh function. And
[23:04] so you need to apply the chat template
[23:05] for the model you're using, but that's
[23:07] all implemented. If it's not implemented
[23:11] properly, you can go in and um like it
[23:13] you ask them and they'll go in and
[23:14] implement it or you do it yourself or
[23:16] something like that. But yeah, it's it's
[23:20] all standardized now. But I I want to
[23:22] people to know that this is going on
[23:23] under the hood because if you don't know
[23:25] this, you can make mistakes and uh and
[23:33] Cool. So um once you have done this uh
[23:38] the next thing is um that you
[23:40] do tool call parsing and actually I'm
[23:42] going to talk about tool called kernel
[23:45] parsing in the next section. So um not
[23:47] immediately here but like let's assume
[23:51] that if uh the language model outputs
[23:53] this you have a way of parsing it into
[23:56] uh into the function arguments. you then
[24:00] um like have the you register the tool
[24:04] at initialization and um you uh have a
[24:08] way to resolve it so that you get a map
[24:10] from the name to the tool that you want
[24:13] to execute. So most agentic frameworks
[24:15] basically will will have a way that you
[24:18] can add new tools. Each tool gets its
[24:20] own name and then you have a Python
[24:22] function or something like that. Python,
[24:24] TypeScript, whatever language. And then
[24:27] it uh it will be dispatched to that with
[24:29] the appropriate arguments. And so then
[24:32] at each time you you parse uh you look
[24:35] up the tool, you validate the uh action
[24:37] from the arguments and you execute uh
[24:40] and then you return. But um at
[24:43] validation time, this can fail if the
[24:45] model gave you the wrong uh the wrong
[24:47] tool call. At execution time, this can
[24:50] also fail if there's like not something
[24:54] that was explicitly said is bad uh is
[24:57] like invalid but implicitly is invalid.
[24:58] So like for example, if you have an
[25:01] execute Python tool, it might accept any
[25:03] string as Python, but then when you
[25:05] actually try to run the Python, it it
[25:06] might fail. So that that would be like
[25:08] an execution error. And then if it does
[25:11] if it well whether it uh whether it
[25:13] fails or not, then uh you get an
[25:21] So this is another detail um that that's
[25:24] pretty helpful but also really annoying
[25:26] uh when you're implementing agents if
[25:29] you if you get it wrong. But basically
[25:33] each tool call is assigned an ID uh when
[25:37] you uh when you run it basically by um
[25:39] uh either the language model inference
[25:42] code or the agent code and then you get
[25:45] a result and the result has a matching
[25:49] call ID and this is useful especially in
[25:51] the case of parallel tool calling
[25:53] because I'm going to talk about parallel
[25:55] tool calling in a bit and having the IDs
[25:57] matched lets you know which tool call is
[25:59] associated assiated with with which
[26:04] result. But the uh the problem is uh for
[26:08] instance uh anthropic if you have a tool
[26:10] call with no matched tool result it will
[26:14] die on you and uh so it will tell you
[26:16] this is an invalid history and I'm not
[26:17] going to accept this history and and
[26:20] generate any more outputs for you. And
[26:24] so in my practical experience there's
[26:25] times when for example the assistant
[26:29] makes a tool call then suddenly uh your
[26:31] your program dies or something like that
[26:32] it fails to write out the tool result
[26:34] and then you resume it it doesn't have
[26:37] the result the associated result and uh
[26:40] anthropic fails to fails to work for
[26:42] you. So this is a little bit of a a
[26:51] Okay. So, um, any any questions there?
[26:57] >> And, uh, great question. Are the tool
[26:59] calls asynchronous? Um, I'm going to
[27:00] talk about that in like the the next
[27:03] next section. Yeah.
[27:06] Cool. Okay. So, now now here's a very
[27:09] technically algorithmically
[27:13] difficult problem. Uh, that may be very
[27:14] interesting to you or maybe not not very
[27:16] interesting to you. But if it's not
[27:18] interesting to you, be glad that other
[27:21] people are solving it for you. Um, so,
[27:24] uh, language models are definitely not
[27:26] guaranteed to generate well-formed tool
[27:29] calls. Um, and this is an example. Uh,
[27:32] you can see that this is JSON that's
[27:36] missing the uh, last closing bracket.
[27:39] So, this is poorly formed JSON. You put
[27:40] this into your JSON parsing program and
[27:42] it will throw an exception and you won't
[27:44] be able to get the uh, the data out of
[27:47] it. So I I've seen a million people go
[27:49] in and try to like figure out if the
[27:50] brackets are missing and like add one
[27:51] post hawk, but you don't want to be
[27:56] doing that. That's not not fun. Um so
[27:58] there's a bunch of constraints uh that
[28:00] you uh could be assigning to each of the
[28:04] tool calls. So the first one is syntax.
[28:06] So it has to be valid JSON. So this is
[28:08] kind of like table stakes, right? So it
[28:11] it needs to parse. Um the second thing
[28:14] is uh shape. So make sure that if you
[28:17] have expected or required fields, you
[28:19] have the required fields. Um the third
[28:22] thing is types. So uh you know if you
[28:26] have city, the city must be a string. Oh
[28:29] sorry. Yeah. Um yeah. So if you have a
[28:32] city, city is a string. Um if you have
[28:34] uh values, uh you know the units are in
[28:36] the appropriate units. So this can all
[28:39] be expressed through um something called
[28:41] JSON schema or basically any schema
[28:46] library. Um so it's like this is a city
[28:48] uh the type is string and the units can
[28:51] be uh Celsius or Fahrenheit and city is
[28:54] required.
[28:57] So um the the good thing about this is
[28:59] this has machine readable validation
[29:01] rules. So you can check if like a call
[29:04] uh follows the schema.
[29:07] But um
[29:09] one way that you can express whether the
[29:12] schema is valid or invalid is by
[29:14] defining a grammar over uh over the
[29:18] schema. And how many people uh did like
[29:22] contextf free grammarss or like context
[29:23] or those sorts of things? Regular
[29:26] grammarss. How many people know regular
[29:28] expressions?
[29:32] Okay. A lot of a lot of people. Okay. So
[29:34] a regular expression is a regular
[29:37] grammar. Um does anybody know how you
[29:44] >> Finite state automaton. Yeah, that's
[29:48] exactly correct. Um so a finite state
[29:50] automaton uh for for those who are less
[30:05] something that looks a little bit like
[30:15] Um, so you have a state and every time
[30:19] you take a token as input, uh, you move
[30:21] to a different state. So if you get A,
[30:22] you would move to this state. If you get
[30:27] B or C, you move to this state. And
[30:30] This this works on uh something called
[30:34] uh uh regular grammarss. So regular
[30:36] expressions like the the slashes and dot
[30:38] stars and stuff like this that you might
[30:42] use to search for search text are uh reg
[30:44] are regular expressions and they can be
[30:47] expressed through regular grammars. Um
[30:49] JSON schema cannot be expressed through
[30:52] a regular grammar. um it can be
[30:53] expressed through something called a
[30:57] contextf free grammar and you can uh the
[30:58] context free grammar can basically make
[31:00] a tree that looks a little bit like
[31:03] this. So um every JSON expression can
[31:05] have brackets on the side. It can have
[31:08] commas between its members. Uh this can
[31:12] be a string um and this can be a unit.
[31:16] And if uh the JSON schema is in the
[31:18] correct format, you should be able to
[31:21] create a tree uh that looks like this.
[31:22] If the JSON schema is in the wrong
[31:25] format, you might create a be able to
[31:27] create create most of a tree. But then
[31:29] when you get to a unit, a unit cannot be
[31:32] K. So basically this would uh this would
[31:36] fail even though a unit can be K, but uh
[31:38] we we defined this to not accept Kelvin
[31:42] as our our unit of temperature.
[31:43] So
[31:47] um basically if you can parse uh the
[31:51] tool call with a contextf free grammar
[31:54] uh defined from your JSON schema you can
[31:56] uh you can do this and I'm not going to
[31:58] go into a lot of details but a finite
[32:01] state automaton cannot parse a um a
[32:02] contextf free grammar but there's
[32:04] something called a push down automaton
[32:05] that can allow you to do this. So
[32:10] basically it adds a stack to uh the
[32:12] regular grammar and uh you push things
[32:14] onto the stack uh pop things off of the
[32:18] stack and eventually can um eventually
[32:20] can decide whether it's uh parsible or
[32:23] not. And so what you do is you start out
[32:26] at the very beginning um with uh a state
[32:28] in this push down automaton and you step
[32:34] through and uh validate your output as
[32:36] you um as you generate it from left to
[32:38] right
[32:41] and I'm giving some examples from X
[32:43] grammar uh and X grammar is a thing
[32:45] that's actually pretty widely used in uh
[32:48] all of the LM inference libraries. It's
[32:49] actually developed by people in the
[32:52] machine learning department here. Uh so
[32:54] what you uh what this means is every
[32:59] time you get an LLM predict the logits
[33:02] of the next token, you take a look at
[33:05] your grammar and if the grammar says
[33:08] this is a valid next token, uh you get a
[33:10] score of one and if you have an invalid
[33:13] next token, you get a score of zero. And
[33:15] you set all of the invalid next tokens
[33:18] to negative infinity. um for the output
[33:21] logits and then you renormalize so that
[33:24] you get probability only on the valid
[33:27] tokens. And so what this uh lets you do
[33:29] is this ensures that you generate valid
[33:31] output.
[33:36] Um, and so
[33:39] this is another figure from the Xgrammer
[33:42] paper and they do these uh tricky things
[33:44] where basically there are some
[33:47] vocabulary that are always valid or
[33:50] always invalid and you premputee these
[33:52] and then there what there are those that
[33:54] are valid only in some contexts only in
[33:56] some uh stack context and then you
[33:58] calculate them on the fly. So it's uh
[34:01] very interesting algorithmically if you
[34:03] like algorithmic uh stuff. If you don't
[34:05] like it uh be glad that the people in
[34:06] the machine learning department are
[34:09] doing it for you basically. Um so
[34:12] because of this almost always um if you
[34:17] are uh if you are have this enabled you
[34:20] will uh and set your appropriate JSON
[34:22] schema you will get wellformed to tool
[34:27] calls. So that that's uh that's great.
[34:29] There's one case where you actually
[34:32] can't uh uh get well-formed tool calls
[34:36] despite this. Um may maybe I can give a
[34:38] quick quiz. This is very very difficult.
[34:39] So I don't know if anybody can get it.
[34:41] But any anybody have an idea where even
[34:44] this would not be uh not be enough. Need
[34:59] Uh I I think that's close enough to what
[35:02] I I wanted to say. So basically um when
[35:04] you run out of tokens, so models can
[35:06] only generate so many tokens and you
[35:08] might run into a place where you're
[35:09] still on a valid path through the
[35:11] automaton, but you're not at the final
[35:13] state. So you generate like part of a
[35:17] JSON output. So very very good. Um and I
[35:19] I've actually encountered this. There's
[35:21] uh theoretically a way you could do that
[35:23] which is like you count the number of
[35:24] output tokens that you still have left
[35:28] and you you cut them off but that's uh
[35:29] if if somebody wants to implement that
[35:31] in next grammar as a extra credit
[35:34] assignment you know be happy to happy to
[35:40] have that okay so now um let's go to
[35:44] rest API calling um so there's uh two
[35:47] different ways to um there's different
[35:49] ways to Express
[35:53] tools and um I'd say probably most
[35:55] people are familiar with REST APIs. The
[35:57] these are the ways you interact with web
[36:01] services. Um but
[36:03] actually sorry there's one other way to
[36:05] call APIs and one way to call APIs is
[36:07] through programmatic tool calling where
[36:09] basically um you just give the model a
[36:12] Python program and you say use the stuff
[36:14] in this Python program to call tools.
[36:16] And so if you do something like that you
[36:19] might have like weather lib.py pi and uh
[36:21] you have the get weather function in
[36:25] here uh with its city and its units and
[36:26] uh then you just say call this function
[36:28] whenever you need to and you give it the
[36:30] ability to execute Python and it will be
[36:32] able to call that tool. So in
[36:34] programmatic tool calling this uh this
[36:37] works but this is not um callable
[36:39] remotely and it's also not callable from
[36:41] the like standard method of tool calling
[36:47] that you use um that you use when you
[36:49] uh implement this uh not through
[36:52] non-programmatic tool calling.
[36:55] So there's a way to turn this into uh
[36:57] REST APIs. Has anybody used fast API
[37:00] before? It's a pretty common Okay. a lot
[37:02] of people. It's a pretty common library.
[37:04] And basically what this allows you to do
[37:07] is this allows you to create a web uh
[37:11] web backend uh extremely simply by just
[37:14] uh setting up a fast API uh giving an
[37:16] API key so you can get people to
[37:18] validate against the API and then
[37:21] writing a Python decorator where uh
[37:26] weather becomes uh becomes this. And so
[37:29] this is good uh for a couple reasons.
[37:31] The first reason is maybe if you don't
[37:34] want people uh looking at the weather um
[37:36] then uh you can prevent them from
[37:37] looking at the weather. But probably
[37:38] more importantly if you don't want
[37:40] people like getting your personal data
[37:42] or something like that you can require
[37:45] an API key and uh this will uh allow you
[37:47] to block anybody who doesn't have an
[37:51] appropriate API key for instance. Um the
[37:55] other reason why is this gives you a
[37:57] JSON schema for free. uh and when I say
[37:59] for free of course you know this is
[38:01] something that's implemented in in fast
[38:03] API but your entire API can be expressed
[38:06] as a JSON schema and that JSON schema
[38:08] can then be provided as is to a language
[38:10] model and that language model can then
[38:12] use it uh to you know specify which
[38:13] calls are allowed and so then you could
[38:17] go in and process this and um whenever
[38:19] the agent made a tool call you could
[38:21] then send it to your API server and they
[38:24] it could use that on the API server
[38:26] Um,
[38:28] another option for calling these is you
[38:31] can just uh use the curl command. And
[38:33] the curl command um basically allows you
[38:35] to call these APIs uh directly like this
[38:37] as well. And so if you have a a coding
[38:40] agent that has access to bash, it has
[38:44] the ability to um to call like this.
[38:47] So this is maybe maybe reasonably
[38:49] straightforward if you're familiar with
[38:51] uh REST and stuff like this. Any any
[38:55] questions or comments or
[38:56] If you haven't played around with fast
[39:00] API, it's nice. It's very easy to use.
[39:02] But um the reason why I wanted to cover
[39:04] this first is this is kind of like the
[39:07] traditional way of of programming uh you
[39:11] know before agents. Um
[39:13] there's uh something called MCP the
[39:16] model context protocol and this was
[39:18] introduced by anthropic uh maybe twoish
[39:21] years ago or a year and a half ago and
[39:24] the idea was this is was designed to be
[39:28] a standard way to uh give your model
[39:31] additional context.
[39:34] When I first saw this I actually was
[39:36] like why do we need to do this? I don't
[39:38] understand why we need to do this. Let's
[39:40] uh let's just let our uh agents call
[39:45] APIs. Um but there is one uh important
[39:48] point about one one or two important
[39:50] points that make MCP different from just
[39:53] calling a normal API. Uh and I'll I'll
[39:55] explain them here. But um first I'll
[39:59] explain why I didn't real I didn't like
[40:00] I thought this was not actually
[40:02] necessary. And basically the reason why
[40:06] is every time you set up an MCP, what
[40:09] you do is you have your AI application
[40:12] and then you set up a couple MCP
[40:14] clients. So like maybe this is your
[40:16] weather client uh your this is your
[40:19] weather MCP and your uh your GitHub MCP
[40:21] or something like that. So you can ask
[40:23] what the weather is what the weather is
[40:32] the reason why I didn't think this was
[40:34] necessary originally was because like
[40:36] why do you need to run a program to call
[40:38] an API, right? We already have good ways
[40:40] to call APIs. We just, you know, send it
[40:43] to the the REST API server.
[40:49] okay. Yeah. So so that's a little bit of
[40:52] an aside. Um, uh, I'll I'll get back to
[40:53] that in a moment, but for a little bit
[40:55] of an aside, uh, there's a really nice
[40:59] library called fast MCP. And fast MCP is
[41:01] basically designed to be fast API for
[41:03] MCP. So if you want to create an MCP
[41:06] server for whatever you want, you can
[41:08] um, just like basically swap out fast
[41:11] MCP and swap it uh, swap out fast API
[41:13] and swap in fast MCP and you can uh,
[41:16] create an MCP server very easily.
[41:19] Um, you can also take in a spec that was
[41:21] generated by like a REST API and just
[41:25] turn it in into an MCP as well.
[41:28] But here here's the main reason why you
[41:32] might want to use MCP uh as opposed to
[41:36] an API. Uh, and the reason why is
[41:38] because it gives you an extra layer of
[41:43] security. And so MCPs have an MCP
[41:48] API key. And this MCP API key uh is
[41:50] something that you need to provide to
[41:53] the process that's running your agent.
[41:54] Separately from this, you have the
[41:56] upstream API key. So like let's say you
[41:59] are getting um getting your agent to
[42:01] connect to your GitHub. The upstream API
[42:03] key would be your GitHub token and you
[42:05] would provide that to the MCP server,
[42:06] but you would not provide it to the
[42:09] agent. And then what you provide to the
[42:12] agent is the MCP API key, which allows
[42:14] you to authenticate into the MCP server.
[42:16] And so the reason why this is important
[42:18] is what happens if you give your agent
[42:21] the GitHub your GitHub token and your
[42:23] agent suddenly decides that it's a good
[42:26] idea to push that to your public GitHub
[42:28] repository.
[42:30] Not good, right? [laughter] Your account
[42:32] gets compromised and uh you get malware
[42:34] installed onto all your repositories or
[42:36] something like this. So you want to give
[42:39] the the agent something that is
[42:42] relatively harmless. Uh so that even if
[42:45] it leaks it for whatever reason like
[42:46] that leak is relatively harmless and
[42:49] then the um the actual credentials get
[42:51] get preserved and so that was basically
[42:58] So um just to go into a summary, they
[43:00] all give you the ability to add a set of
[43:04] APIs into uh into your agent. Like you
[43:05] could do that through a regular JSON
[43:09] schema or through an MCP. Um
[43:11] the uh but a lot of other things are
[43:13] different. So like for discovery um you
[43:16] might need to fetch an open API uh
[43:19] document. For MCP there is a special API
[43:20] that allows you to list all of the
[43:26] tools. Um for invocation um you call an
[43:27] HTTP
[43:31] uh thing here for um MCP there's an MCP
[43:33] transport and this can be through
[43:34] various ways. You connect through
[43:36] standard IO or you connect through an H
[43:39] uh uh a socket or something like that.
[43:42] Uh I already talked about authentication
[43:46] and um MCP actually has a few other um
[43:48] has a few other like conveniences like
[43:50] you can add resources, prompts and
[43:51] extensions, but I'm not going to go into
[43:59] Cool. Um
[44:01] actually, um there's two other things
[44:03] I'd like to mention. um there I don't
[44:08] want to uh I I guess I forgot to add
[44:11] them to my slide. Um so the first thing
[44:16] is um MCP registry. There's an official
[44:20] MCP registry. So if you want to find
[44:22] MCPS uh that allow you to do something
[44:24] like this, you can, you know, go to this
[44:27] registry and find uh any of a very large
[44:30] number of MCPS. There's also like a
[44:34] million and a half uh MCP server like
[44:36] websites that you can go to that are are
[44:39] ranked based on uh popularity and stuff
[44:42] like this. Another thing is um I've been
[44:43] talking a lot about the Pittsburgh
[44:47] weather and uh the funny thing is uh
[44:49] today I prepared all of these slides
[44:52] like earlier of course but today we
[44:54] actually got Pittsburgh weather that was
[44:56] simultaneously rainy and sunny at the
[44:59] same time. And so I managed to break my
[45:01] own API because it cannot return
[45:03] multiple states at the same time. But uh
[45:05] uh yeah, it was uh quite the
[45:06] coincidence. You can see the torrential
[45:08] downpour and the the bright side at the
[45:12] same time. Okay. Uh back back to serious
[45:19] Cool. Um so another big uh kind of like
[45:22] development pretty recently is parallel
[45:25] tool calling. in parallel tool calling.
[45:28] Um the the basic problem we want to
[45:29] solve is the same problem that I talked
[45:31] about when I talked about like the codec
[45:33] and the programmatic tool calling which
[45:38] is if you call tools one at a time. Um
[45:41] the uh it it could become very long for
[45:42] even a simple operation because you
[45:43] might do a weather and then do a
[45:47] calendar and then do a flight. Um, but
[45:49] if tool calls are independent, you can
[45:51] actually call them at the same time. And
[45:54] this is done pretty simply. You just
[45:59] like add add multiple tool call
[46:07] The um there's a few nuances about this.
[46:09] The first one is um you can only
[46:11] paralyze tool calls if they don't have
[46:14] dependencies on each other. So, um, like
[46:15] if you were looking up the weather for
[46:16] Pittsburgh and reading today's calendar
[46:19] and looking up flight status, that might
[46:21] be, uh, might be good. Um, but if you
[46:23] need to find a customer ID, use it to
[46:25] fetch orders and refund the selected
[46:27] order. Obviously, you can't do that. So,
[46:28] there's limits to the parallel tool
[46:30] calling you could do. And if your
[46:32] calendar or your flight was dependent on
[46:33] the weather, then you know, obviously
[46:37] that'd be a problem, too.
[46:39] So, there was a question about this. Um,
[46:40] do you execute the tool calls in
[46:42] parallel? And the answer is typically
[46:46] yes. You can just uh use typical Python
[46:48] uh syntax to you know have a whole bunch
[46:51] of tool calls and then execute them and
[46:52] then uh use something like
[46:55] async.io.gather to uh to return the
[46:58] results of them when they run in the
[47:01] same time. So this is uh uh this is
[47:03] pretty common. Another thing I'd like to
[47:07] point out is um this is a major
[47:10] difference between really efficient
[47:12] language models in note efficient
[47:15] language models. And
[47:18] there there's this weird
[47:20] weird paradox in agentic language models
[47:25] nowadays that more expensive models more
[47:27] expensive models can actually be cheaper
[47:29] if you measure them on a taskbytask
[47:31] basis. And there's two major reasons for
[47:33] this.
[47:35] The first major reason is more expensive
[47:37] models can be smarter. So they pick like
[47:40] an appropriate solution more quickly. Um
[47:43] but another thing is um more recent
[47:45] models
[47:47] do parallel tool calling uh a lot
[47:49] better. So they make a whole bunch of
[47:51] calls at the same time. So if you're
[47:53] using a coding agent or something like
[47:57] this, uh you use the the better uh you
[47:59] use the better models and they are doing
[48:02] like a bunch of view images at the same
[48:05] time or they're uh like writing a bunch
[48:07] of different files at the same time or
[48:08] something like that. That's because
[48:09] they're doing parallel tool calling.
[48:12] Well, um does anyone have an idea of
[48:14] like why they got so much better at
[48:16] this? They like this was not a huge
[48:18] thing even though parallel tool calling
[48:20] mechanisms have existed for a long time.
[48:22] This was not a huge thing until maybe
[48:25] like six months ago or something. Yeah.
[48:26] >> Reinforcement learning just forced them
[48:27] to do that.
[48:29] >> Yes. Exactly. So reinforcement learning
[48:31] uh kind of forced them to do that and so
[48:33] the models were very heavily
[48:35] incentivized to fish finish tasks
[48:37] quickly and parallel tool calling is one
[48:40] of the good ways to do that. So if you
[48:41] do reinforcement learning with a very
[48:44] heavy like brevity penalty on on how
[48:47] long uh the task execution is, you can
[48:50] get uh like a lot more parallel tool
[48:57] Cool. So um the final thing I'd like to
[48:58] talk about in this lecture today is
[49:02] evaluating tool use. And so I'm not
[49:05] going to talk about evaluating endto-end
[49:08] agentic tasks immediately yet. um but
[49:10] rather talk about evaluating just the
[49:12] tool usability of language models
[49:15] because it's kind of like a prerequisite
[49:18] for language models to be good at um uh
[49:21] good at agentic tasks. And there's a
[49:24] bunch of data sets for this. The most
[49:25] famous one is the Berkeley function
[49:28] calling leaderboard and this has four
[49:31] versions. Uh it started out with version
[49:35] one which was basically um single turn
[49:38] uh tool calling. Um it's then evolved
[49:39] through the four versions and now it
[49:42] covers um multi-turn tool calling. It
[49:44] also does have aentic tool calling but
[49:47] this is more um not for like endto-end
[49:48] coding agents or something like that.
[49:51] It's uh tool calling agents and they
[49:53] also have tool calling robustness. So
[49:55] they measure um hallucination of
[49:57] arguments. They also measure format
[49:59] sensitivity. So when I talked about like
[50:01] the all the different formats uh they
[50:09] So um
[50:11] when you uh go in to evaluate the whole
[50:14] uh stack there's a number of things that
[50:17] you want to uh evaluate. So the first
[50:20] thing is did the language model choose
[50:22] the appropriate tool for the task. So it
[50:24] might have picked like a an
[50:27] inappropriate tool that can't uh allow
[50:30] you to do that uh the task at all. Um
[50:33] the other thing is arguments uh which is
[50:35] uh you know whether you you add the
[50:38] right values. Um if you're talking about
[50:40] agentic tool calling you can talk about
[50:42] whether it did it in the right order and
[50:44] then you can uh measure endto-end task
[50:46] accuracy for if you're doing uh agentic
[50:48] tool calling. And all of these are kind
[50:54] Then separately from that there's also
[50:57] um efficiency. So like uh how quickly
[50:59] can you solve the task? Like um how many
[51:01] tokens did it take? How how much did it
[51:06] cost? Um reliability. So um you know if
[51:10] a tool call times out uh does it retry
[51:12] appropriately? If a tool is out of
[51:15] order, can it choose a a different one?
[51:17] And also um safety. So if you have
[51:20] adversarial outputs where you ask it to
[51:23] use a tool in an inappropriate way, uh
[51:24] can you do this? And all of these are
[51:26] like over the four iterations of this
[51:28] benchmark. It covers uh all of these
[51:34] Um yeah, I kind of covered that already
[51:37] actually. So one other uh really
[51:39] interesting benchmark uh for tool
[51:43] calling is uh this open router uh tool
[51:45] call air rate benchmark. I don't know if
[51:48] anybody like uses open router or has
[51:51] seen this before. Maybe no.
[51:56] Okay. So um this is for the same model.
[51:58] All of these are for uh I think this is
[52:02] GLM 5.3. So it's like the same the same
[52:04] model and it's measuring the tool call
[52:07] error rate
[52:10] simply the only thing they varied is who
[52:14] serves the model to you. And this is uh
[52:16] this is pretty important obviously
[52:18] because you think oh I'm going to use
[52:20] this model maybe you know it's going to
[52:22] be the same regardless of who provides
[52:24] it to me but actually the difference is
[52:28] between 15% and like 0.01
[52:30] to 0.05%.
[52:42] There were some uh there were some hints
[52:44] in the lecture and some uh not some
[52:45] hints in the lecture
[52:47] >> is decoding algorithms different maybe
[52:50] someone's using
[52:52] like cheaper version of the model or
[52:54] quantized version of the model.
[52:56] >> Yeah, great great points. So I'll I'll
[52:59] repeat it. So number one is the decoding
[53:00] or the inference algorithm could be
[53:03] different and um one very big difference
[53:05] is whether they're using quantization of
[53:07] the model or not or like what level of
[53:09] quantization of the model they're using.
[53:14] So my my personal experience is um uh
[53:17] FP8 models uh FP8 is kind of like the
[53:19] default level of uh quantization for the
[53:23] model um get a lot fewer uh mistaken
[53:25] tool calls than FP4 models because FP4
[53:28] is like compressing it very heavily.
[53:29] It's saving money for the inference
[53:33] provider, but it's it's usually a worse
[53:35] model. There aren't very many FP4
[53:37] quantizations that can allow you to get
[53:40] the same performance. Another one was uh
[53:42] speculative decoding. Um I don't think
[53:43] we're going to talk about speculative
[53:45] decoding a huge amount in this class.
[53:46] Maybe I'll talk about it during long
[53:50] context or actually may there are a few
[53:52] algorithms specifically for agents which
[53:53] are interesting. So maybe we can talk
[53:55] about it. But basically what it is is
[53:58] you have another cheaper model um that
[54:00] predicts what the more expensive model
[54:02] is going to do and then you use that to
[54:04] like speed up your inference.
[54:08] um spec lossless speculative decoding
[54:09] probably shouldn't make a difference
[54:13] because it it's like not changing the
[54:15] underlying result of the model. But if
[54:16] they're doing some sort of like lossy
[54:19] speculative decoding uh then that might
[54:20] might cause it to be different. But then
[54:22] you know calling it the same model is
[54:25] also probably a bad uh a bad idea. Uh
[54:27] there's one other thing um that I
[54:31] mentioned uh and anybody have an idea
[54:34] this was actually mentioned in the uh in
[54:46] What can you do to make your tool calls
[54:48] more successful?
[54:50] >> Yeah.
[54:52] >> Constraint decoding. Yeah, exactly. So
[54:54] these different providers might be using
[54:55] different constraint decoding
[55:00] algorithms. Um just practically
[55:03] many many of these providers will be
[55:05] implementing their own inference
[55:07] algorithm. So they'll have their own
[55:08] inference algorithm completely
[55:11] implemented from scratch. Um some of the
[55:13] providers will be using an open source
[55:16] one like VLM or SGLANG. And VLM or SG
[55:18] lang support different grammar-based
[55:22] decoding uh algorithms. And so uh some
[55:24] of these providers just might not have
[55:26] that implemented and so they're entirely
[55:27] relying on the language model to do good
[55:31] tool calls. Um otherwise uh they might
[55:33] not. A final kind of like boring reason
[55:35] why tool calls might fail is the
[55:37] inference provider might be unreliable.
[55:39] So it might go down some of the time and
[55:47] Cool. Um so these are the um that that's
[55:49] the main thing that I I had for today.
[55:51] Um so tool use is basically a layered
[55:54] system. Um you know the tools add
[55:56] capabilities such as retrieval,
[55:58] execution, generation, application.
[56:01] They're what make an agent an agent. Uh
[56:04] but we can't get that uh for free. And
[56:08] um you can uh add schemas to the prompt.
[56:10] Uh the models emit calls and then you
[56:13] validate dispatch and match results by
[56:16] ID. And we can add constraints uh like
[56:18] grammar-based decoding. um they don't
[56:21] guarantee semantic correctness. So um if
[56:22] you have like a Python program, the
[56:24] Python program might still be wrong even
[56:26] if you generated uh you know a string
[56:29] that could be parsed as Python. Um and
[56:31] there's a number of uh ways you can
[56:33] interface with them like direct rest
[56:35] calls and MCPS.
[56:37] Uh and then we have a lot of systems
[56:39] that um orchestrate dependencies and
[56:43] concurrency and uh allow us to evaluate.
[56:46] So yeah, that that's uh what I wanted to
[56:48] talk about for tool calling. Uh this
[56:49] will be something that is covered in the
[56:51] harness uh assignment or the first
[56:53] assignment where you build your agent.
[56:54] So you'll need to need to deal with
[56:58] this. Um but and next time we're going
[56:59] to talk about context management for
[57:03] long context in long context LMS. But um
[57:05] any questions
[57:07] to wrap up?
[57:08] Okay. Yeah. Yeah. And I'm going to
[57:10] repeat in case people didn't hear in the
[57:13] back, but the first um uh assignment for
[57:15] reflecting on the lecture and talking
[57:16] about something you learned in the
[57:18] lecture is going to be up on Canvas. So,
[57:20] make sure you uh make sure you submit
