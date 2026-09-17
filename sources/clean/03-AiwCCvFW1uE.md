# CMU AI Agents 2026: 3. Long Context Modeling for Agents

- Видео: https://www.youtube.com/watch?v=AiwCCvFW1uE
- Длительность: 1:15:39
- Дата публикации: 20260908

## Расшифровка

[00:09] Okay. Uh hello everyone. Can you hear me
[00:11] in the back?
[00:15] All good. Okay.
[00:20] So, uh well, welcome back everyone.
[00:24] Am I uh echoing? All good. Okay. So, um,
[00:26] today I'd like to talk about context
[00:30] management for long context agents. And
[00:33] I at first thought about titling this as
[00:35] like context management for long context
[00:37] LLMs because most of the stuff I'm going
[00:38] to be talking about today is kind of
[00:41] more general LLM stuff, but long context
[00:44] is super super important for when we're
[00:45] working on agents and it's not
[00:47] necessarily covered uh, very well in all
[00:49] of the LLM prerequisite classes. So, I'm
[00:51] going to cover it in a fair amount of
[00:53] detail today. I'm also going to try to
[00:55] go through kind of the long context
[00:58] architectures that are used in many of
[01:00] the kind of state-of-the-art open uh
[01:03] models so you can kind of see the best
[01:05] practices that everybody is using in
[01:12] So first I'd like to talk a little bit
[01:16] about um how long an agent context can
[01:17] grow.
[01:22] So basically the input is quadratic uh
[01:26] from the uh or the number of token
[01:29] accesses that you do is quadratic uh
[01:31] based on the linear history growth. So
[01:35] um if each call uh you make for an agent
[01:36] takes about you know five tokens and
[01:38] let's say you start out with a an
[01:40] initial system prompt of one token uh
[01:42] you'll get six tokens in the first call
[01:47] 11 16 uh 21 and 26. you know, this will
[01:50] increase and increase and increase. Um,
[01:53] and so by the time you have gotten to
[01:55] the end, you will, if you do things
[01:59] completely naively, you will have had to
[02:02] process ADK tokens uh for these five
[02:06] calls. And you know, this can continue
[02:08] for a very long time. I I don't know the
[02:10] longest anybody has used a single coding
[02:11] agent session or something like that,
[02:13] but I've certainly done them for like
[02:15] multiple days uh where I've been working
[02:17] with it for almost the entire day. So
[02:19] you could imagine this could get uh very
[02:22] very large. Um the actual computational
[02:27] complexity of this is uh is actually
[02:30] even larger than this. Um
[02:33] well no sorry. So yeah the the
[02:35] computational complexity is is quadratic
[02:37] here.
[02:40] So why do agent prompts get so long uh
[02:43] so quickly? I did a little bit of data
[02:47] analysis on uh the composition of
[02:51] prompts that I used in um uh 1,500
[02:54] sessions from our uh coding agent
[02:57] openhands. And
[02:59] each each session was relatively short.
[03:01] These are not like the long multi-day
[03:03] sessions that you do. This is more like
[03:06] solving a single task. But uh each one
[03:10] used about 78,000 tokens on average. Um
[03:12] 23% of this was a system prompt in all
[03:14] of the tool descriptions. Uh this is
[03:16] relatively large for a coding agent. I
[03:18] think our system prompt is somewhere on
[03:21] the order of like 15,000 to 18,000
[03:23] tokens because we're very opinionated.
[03:25] Uh the open ants agent is very
[03:27] opinionated about how people uh do work.
[03:30] Um these tend to vary from like 8,000 to
[03:33] uh 8,000 to 20,000 tokens depending on
[03:35] you know how many tools you uh you pull
[03:38] in and stuff like this. Um separately
[03:41] from this uh 9% were user messages. So
[03:42] this is the user either saying the
[03:45] initial task or following up with uh
[03:48] additional information after that. 9%
[03:51] were reasoning traces um and you know
[03:53] where the model is thinking through
[03:56] things. 2% were model replies. Sorry,
[03:58] this isn't showing on the slide, but 2%
[04:00] were um the model replying directly to
[04:03] the user. So, it's spending about um
[04:05] five times as many tokens freezing as it
[04:07] is spending communicating uh with text
[04:10] to the user. And 20% were tool calls. Uh
[04:14] so, you know, uh you know, writing code,
[04:16] uh reading code, that sort of thing. And
[04:19] 37% were tool results. So, this is uh
[04:21] you know, getting the result of, you
[04:22] know, reading a file or something like
[04:23] this.
[04:27] So you know each step can uh will
[04:29] consist of all of these and that tends
[04:35] So when you're handling this very long
[04:38] context uh there's two big challenges
[04:42] here. Uh the first one is capacity and
[04:44] so whether your model is able to handle
[04:45] this large amount of uh evidence in the
[04:49] first place and this is a challenge uh
[04:50] because as I'll talk about in a little
[04:52] bit training models to handle very long
[04:54] context is hard
[04:57] um and so in order to manage this you
[04:58] need uh things like architecture
[05:01] position encoding training data uh and
[05:03] uh you also need to be able to evaluate
[05:05] whether you're doing a good job of this.
[05:08] And then the second thing is efficiency
[05:10] uh and whether the system can afford to
[05:12] serve it. And there's a bunch of
[05:16] techniques to do that as well. And I I
[05:17] think some people might be taking this
[05:19] for granted if you're just using, you
[05:20] know, cloud code or codeex or something
[05:23] like this, but they're doing some pretty
[05:26] monumental feats of engineering to take
[05:29] a, you know, multi- trillion parameter
[05:34] model and serve it within seconds uh to
[05:36] uh over and over and over again for mil
[05:38] I don't know codeex has 25 million
[05:41] users. So you can imagine uh 25 million
[05:43] daily users hitting it every few seconds
[05:46] for this huge model. Uh if you want to
[05:48] you can calculate in your head how many
[05:51] flops per uh per second that might be.
[05:59] Cool. Um so any questions or things?
[06:01] Probably pretty straightforward I guess.
[06:06] Okay. So uh let's go into inference. And
[06:11] so in order to make this happen uh the
[06:15] you basically need to be able to um
[06:19] calculate uh prefill and decoding. So uh
[06:21] calculate your inputs and your outputs
[06:26] at each step. And this uh you know I'm
[06:28] sure everybody has done in your previous
[06:31] classes uh for generating from uh you
[06:33] know a language model. some things you
[06:34] may or may not have thought about in
[06:36] your previous classes. If you took how
[06:39] many people took like uh language model
[06:41] systems or deep learning systems or
[06:43] something like that actually more than I
[06:44] thought. So if you took the systems
[06:47] course you you probably handled this. Um
[06:48] but other things you need to think about
[06:51] are how do you schedule uh multiple
[06:53] concurrent queries? Um and also how do
[06:56] you save the results in the KV cache uh
[06:59] so you can reuse them and not have to
[07:01] reuse them over and over again. uh not
[07:05] have to calculate over and over again.
[07:08] So going into a bit more detail here, um
[07:11] we have a few phrase uh phases in
[07:12] inference. The first one is called
[07:14] prefill. Um you could also call it
[07:17] encoding. Um but I think pre prefill is
[07:20] kind of the like preferred term of art
[07:24] nowadays. And so you take in all of your
[07:26] input tokens uh that you don't need to
[07:29] generate and uh you generate the key and
[07:33] value pairs uh from each of them. And
[07:35] then uh when you're decoding you
[07:38] basically uh take the prompt uh and key
[07:41] value pairs um generate an output and
[07:43] append uh the key value pair that you
[07:46] get from the output. So um you do this
[07:48] kind of incrementally whereas this can
[07:55] And so uh when we think about this as a
[07:57] serving system, there's a bunch of ways
[08:01] we quantify how good a serving system
[08:04] is. Uh the first one is time to first
[08:07] token. So this is how long you need to
[08:10] start um you need to wait between when
[08:13] you start uh
[08:15] entering a query and when you start
[08:17] seeing the first output. And so like I'm
[08:20] sure everybody you know who uses chat
[08:22] GPT or something like that uh you put in
[08:24] a long output you notice it takes longer
[08:25] to start getting a response than if you
[08:28] put in sorry put in a long input you see
[08:30] it takes longer to start getting a
[08:31] response than if you put in a short
[08:33] input and that's like your TTFT is
[08:37] higher. Uh then uh your time per output
[08:41] token is the uh time like the amount of
[08:43] time it takes uh between generating each
[08:47] token. And if you go to a website like
[08:52] um
[08:56] t typically uh here this will be your
[09:00] time per output token there I am pretty
[09:02] sure they're not counting prefill here
[09:04] and it's just like the time between uh
[09:05] each of the tokens that might be a
[09:07] little bit small with the black
[09:09] background but you can see that um for
[09:14] GLM 5.2 to uh you have like 63, 48, uh
[09:17] 24, uh that sort of thing. And you know,
[09:19] some providers are drastically better
[09:22] than others. Like this provider,
[09:24] not to pick on Mistl, but they're
[09:26] getting, you know, three three tokens
[09:29] per second and then these other ones
[09:31] like Parasel and Coreweave are getting,
[09:32] you know, hundreds of tokens per second.
[09:38] So um so basically uh you know this
[09:39] makes a huge difference in your
[09:44] experience using um uh using agents. Uh
[09:47] one other interesting thing is um
[09:49] there's different ways people can use
[09:52] agents. And so in some cases you might
[09:54] really hear about this. So like let's
[09:58] say you're working together um with a an
[10:01] agent on a interactive task in your
[10:02] favorite coding CLI. you may really
[10:04] really care about, you know, TTFT and
[10:08] Tapot. Um, if you're running an agent in
[10:10] the background to do some background
[10:12] tasks that run overnight, you might not
[10:15] care at all. Um, and there's trade-offs
[10:17] between them, between like throughput
[10:20] and cost and how fast uh you can get the
[10:24] the tokens. And like I you know also um
[10:27] serve coding agents uh with my company
[10:29] and when I talk to providers they'll
[10:31] often often ask which do you care about
[10:33] more so we can optimize the system uh
[10:35] for the one you care about more and so
[10:37] um there's uh there's ways you can do
[10:47] Cool.
[10:50] Um yeah so sorry just to finish the
[10:53] slide. So throughput is um the completed
[10:54] tokens or requests divided by the wall
[10:56] clock time. So this is kind of seen
[10:58] usually on a more holistic level over
[11:01] the whole system. And then uh the cost
[11:04] is you know how much it costs.
[11:08] So as a refresher um I I hopefully
[11:10] everybody should know this already. Um
[11:14] but you have uh the
[11:18] uh query key and value calculation in uh
[11:22] typical attention and this is uh so you
[11:23] have this here and then you take the
[11:26] softmax um divide it by this. You might
[11:29] have some sort of uh you know positional
[11:31] uh bias and then you calculate your
[11:35] output and typical full attention uh
[11:37] looks uh like this. you mask all the
[11:40] previous tokens and and or you consider
[11:41] all the current tokens and you mask all
[11:44] the um the future tokens.
[11:48] Um so this is of course very expensive
[11:50] because it's quadratic in the sequence
[11:53] length. Uh and so a lot of the stuff I'm
[11:54] going to be talking about today is about
[11:56] how to fix that.
[11:59] Um so this is on the efficiency side and
[12:02] then on the effectiveness side just
[12:05] because you have a model or just because
[12:06] you have a serving system that can take
[12:09] in you know a million tokens doesn't
[12:12] necessarily mean that you can use that a
[12:15] million tokens effectively and
[12:19] um this is a very like old school
[12:21] example of this I guess this is a needle
[12:23] in the haststack evaluation how many
[12:25] people have seen this figure for
[12:28] maybe some but not not that many. Okay,
[12:30] so to explain what this looks like,
[12:34] basically what this is saying is um it's
[12:36] a very weird evaluation. Basically, they
[12:38] um they took a whole bunch of Paul
[12:40] Graham essays uh by the like famous
[12:42] entrepreneur and head of Y Combinator
[12:45] Paul Graham and they stuck in uh
[12:46] something about like the best place in
[12:48] San Francisco to eat a sandwich is
[12:50] something or other and then they ask a
[12:52] question where's the best place in San
[12:54] Francisco to eat a sandwich and then the
[12:55] language model has to answer that
[12:58] correctly. um and they made the context
[13:00] longer and longer and longer and then
[13:03] they evaluate uh models with the longer
[13:06] context and eventually the weaker models
[13:08] start getting worse at these very very
[13:10] long contexts and there's a bunch of
[13:13] examples of things like this. Um ruler
[13:15] and helmet are kind of the the common
[13:18] benchmarks that people use here. Um but
[13:21] basically uh the long the summary is
[13:24] that if you have very long context your
[13:25] models might start getting worse at
[13:28] processing them.
[13:29] So has anybody noticed this when you've
[13:31] used a coding agent for a long time like
[13:34] are there common
[13:36] or used any agent for a long time are
[13:38] there common like failure cases that you
[13:40] see?
[13:42] What what kind of things what kind of
[13:45] things have bothered you?
[13:49] >> Yeah.
[13:51] >> Forget the previous context.
[13:53] >> Yeah. Forgets the previous context. Did
[14:08] with me telling it not to do something
[14:09] in the middle of the conversation and
[14:13] then it goes and does it. Um there there
[14:16] was a really bad example uh where I
[14:17] think actually Daniel talked about it
[14:19] here where the person had said do not
[14:21] delete this and then it went and deleted
[14:22] it anyway because it had forgotten the
[14:25] context. So yeah, this can be a really
[14:28] big problem in agentic settings because
[14:29] you know the user is giving these
[14:33] incremental instructions. So
[14:35] so I'm going to be talking about several
[14:36] different things. I'm going to be
[14:37] talking about architecture. I'm going to
[14:40] be talking about training inference and
[14:43] compaction. So going first into
[14:46] architecture. Um this is both about
[14:49] efficiency and accuracy.
[14:51] And so as I mentioned standard attention
[14:53] is global. So it makes pairwise
[14:57] comparisons across uh all of the tokens
[15:02] here. And um the problem with this is uh
[15:07] like this is quadratic obviously. And
[15:09] does anyone know the like standard
[15:13] length of the of models nowadays of
[15:15] these uh of like state-of-the-art
[15:17] language models?
[15:19] >> 256 to a million.
[15:21] >> 256 to a million. Yeah. And I I'd say
[15:23] most people are aiming for a million now
[15:24] because they don't want to be the, you
[15:27] know, the model that has 256 when
[15:29] everyone else has a million. So very
[15:30] quick math in your head, how many
[15:34] pairwise comparisons is that?
[15:35] >> 10 12
[15:38] >> 10 10^ the 12 or in English.
[15:41] >> A trillion. Yeah, that's a trillion.
[15:43] That's a trillion comparisons every
[15:45] time. uh like when you're uh generating
[15:49] a sequence of a million long and each
[15:53] comparison uh requires you to multiply
[15:55] large vectors by each other over and
[15:56] over and over again. So you're starting
[16:01] to get up into the you know 10 to the
[16:06] I guess it'd probably be 10 to the 20ish
[16:08] uh which is a lot that that's a lot of
[16:12] compute um for a single sequence.
[16:16] So um there there's ways that people
[16:19] solve this and basically almost all of
[16:20] them fall into the category of taking
[16:23] this quadratic computation and putting
[16:24] some sort of constant limit on the
[16:27] number of comparisons that are made uh
[16:30] at each time step. And that brings your
[16:34] uh n squared down to owl where I I wrote
[16:36] w for window but it doesn't necessarily
[16:38] need to be a window. It just needs to be
[16:39] the cap on the number of comparisons
[16:47] Um so there's the idea of local models
[16:49] and global models. And so local models
[16:51] are are basically models where this cap
[16:54] on computation happens within a local
[16:57] window. And then global models you have
[16:59] a cap on you might or might not have a
[17:01] cap on computation but that cap on
[17:03] computation is not localized. So you can
[17:05] pass information uh throughout the
[17:09] entire sequence. And the I'd say almost
[17:12] all of the models uh that exist nowadays
[17:14] or are widely popular nowadays are some
[17:17] variety of hybrid model where they have
[17:20] many local computations and then one
[17:21] global computation then many local
[17:25] computations one global computation
[17:27] and specifically I'm going to talk about
[17:31] six uh models that we have here. So uh
[17:34] the most recent Quen model uh has uh
[17:37] local computation of uh gated delta net.
[17:39] I'll explain all of these uh or most of
[17:41] these in a bit. And then um sparse
[17:44] retrieval uh for the global computation
[17:46] and the ratio is 3:1.
[17:51] Uh GLM 5.3 is uh also a variety of delta
[17:56] um and sparse attention uh with 3:1.
[17:58] Um
[18:03] uh Kim K3 is uh a variety of Delta and
[18:07] um this is a dense uh dense attention
[18:08] 3:1.
[18:12] Uh Neimotron is Mamba uh which is uh
[18:15] kind of like recurrent style model
[18:19] and uh dense attention 4:1.
[18:22] um to uh window uh sliding window
[18:25] attention uh dense attention 5 to one
[18:28] and deepseek's a little bit different.
[18:31] It kind of has uh window windowed
[18:34] attention but then some uh sparsity uh
[18:37] sparse stuff with interle branches. So
[18:40] um basically the the standard way of
[18:43] doing things is hybrid model uh with
[18:45] some sort of local thing and uh either
[18:49] sparse or dense uh global attention.
[18:51] So I'm I'm going to be talking about
[18:53] this. I'm not going to go into like a
[18:55] ton of details for all of them, but uh
[18:56] it should be enough that you could be
[19:02] So the first one is uh sliding window
[19:05] attention. And this is maybe the the
[19:08] simplest conceptually. And what you do
[19:12] is you take chunks or uh you take chunks
[19:15] of the output and basically you're able
[19:19] to attend to your current chunk and um
[19:24] all of the previous chunks and uh
[19:25] or not all of the previous chunks, a
[19:27] fixed number of previous chunks. So if
[19:30] this is your current chunk, um it might
[19:32] be a chunk of like 512 tokens or
[19:34] something like this. You would have an
[19:36] additional 512 and 512 tokens in the
[19:38] previous chunks and you would attend to
[19:42] those. Um so pretty simple, no changes
[19:44] to attention, but you have something
[19:46] like this. But the nice thing about this
[19:49] is on the first layer you're passing
[19:51] information from the previous one or two
[19:54] chunks, but on the next layer the uh
[19:55] previous chunks also have information
[19:57] from their previous chunks. And so you
[19:59] kind of get this gradually expanding
[20:02] window. Um
[20:05] so uh this uh this is pretty widely
[20:11] Um but the more popular way of doing
[20:14] things nowadays is using some variety of
[20:16] linear attention.
[20:19] And so the way uh linear attention works
[20:23] is basically we take our uh standard
[20:25] attention and standard attention has
[20:28] this um softmax operation included in
[20:31] it. And this is the reason why it's hard
[20:32] to compute because you're taking the
[20:36] exponent and um and dividing. And
[20:38] because you do this there's you
[20:41] basically have no choice but to expand
[20:47] all of the uh key and query computations
[20:49] uh like key query multiplication
[20:53] computations in and be uh quadratic uh
[20:55] quadratic
[20:57] complexity.
[20:59] What linear attention does is you
[21:03] basically start from this uh kind of
[21:06] standard attention formulation but you
[21:09] take you remove the softmax and the
[21:11] normalization here or I mean the
[21:13] normalization doesn't really matter but
[21:16] you remove the softmax and you get just
[21:19] the key query multiplication
[21:21] and [clears throat]
[21:24] this is definitely less expressive
[21:25] because basically what you're doing is
[21:27] you're moving
[21:29] from something that
[21:54] Anyway, like pretend pretend that this
[21:56] bottom one adds up to one, but you're
[21:58] going from a thing that takes a bunch of
[22:00] real numbers and normalizes them into
[22:02] probability like numbers that are
[22:06] between zero and one and add to one. Um,
[22:08] so this nonlinearity allows you to focus
[22:12] on like only some of the previous uh
[22:14] like tokens. And this is kind of the
[22:15] good point of attention. That's the
[22:16] selling point of attention that allows
[22:19] you to focus on the relevant previous
[22:21] context. And you're basically taking
[22:24] away that ability, right? You're you're
[22:26] removing the relative comparisons and
[22:28] just getting um the the dotproduct
[22:31] between the queries and keys. But it
[22:33] allows you to do something really uh
[22:37] nice which is that you can use uh the
[22:38] associative
[22:41] uh you can use associivity and basically
[22:43] rearrange
[22:49] so that um you can convert the sum of
[22:53] all the key and value uh multiplications
[22:56] before into a single uh state matrix.
[22:59] And so this state matrix is essentially
[23:02] a function that map it's a linear
[23:05] function that maps from a query to a
[23:08] value. So attention is also a linear
[23:10] function that maps from a query to a
[23:12] value. So if I go back to this here
[23:14] you're basically calculating you're
[23:16] taking the query you're calculating the
[23:18] attention over all the keys you're
[23:20] multiplying it by the values and you're
[23:24] getting a value here. Um and this state
[23:27] matrix is also that. But the nice part
[23:29] about it is this state matrix can be
[23:32] decomposed. So you can update it. You
[23:34] can keep this state matrix around and
[23:36] update it in constant time every time
[23:38] you get a new value. So this essentially
[23:40] becomes like a recurrent neural network.
[23:43] So it it allows you to update the state
[23:47] matrix um in linear time without having
[23:49] uh without requiring the quadratic
[23:50] computation.
[23:52] So
[23:54] this basically solves your quadratic
[23:57] problem and it solves it so much
[24:00] that um O of N squ becomes O of N.
[24:03] There's no like there's no even W term
[24:06] in this because uh each time you're uh
[24:08] you're updating based entirely on the
[24:11] previous state. Um but there's there's
[24:14] caveats here. So um is this clear though
[24:17] uh so far?
[24:19] Okay, cool.
[24:21] Um, so the big caveat is exactly the
[24:23] caveat I mentioned before. Like this is
[24:26] just a less expressive function. Um, and
[24:27] it doesn't allow you to make like
[24:29] relative comparisons between the
[24:32] previous tokens, that sort of thing. So
[24:35] there's a bunch of uh workarounds around
[24:39] this to try to make a more expressive
[24:41] function that nonetheless is useful in
[24:44] um in kind of uh doing attention-like
[24:49] calculations. And so um most of these
[24:50] are
[24:53] if you dig deep into the math in them,
[24:54] they're basically trying to become
[24:56] better predictors of the final value
[24:59] that you would get from attention. Um
[25:01] and you you can dig into the papers to
[25:02] see how that works, but I'm going to
[25:05] explain them mostly uh mechanistically
[25:07] here. And so um the first thing is
[25:11] Delta. And the idea behind deltaNet is
[25:16] um you can predict what
[25:18] um
[25:21] you can essentially predict what value
[25:25] you would want to be getting from the uh
[25:30] from the calculation of uh KT
[25:36] um and S. And so you know KT here is uh
[25:40] the key at time step t and you are
[25:42] comparing it with the matrix at time
[25:46] step t uh t minus one and uh you're
[25:51] calculating this v hat t and
[25:57] on the other hand you um so basically
[25:59] this this is the prediction that you
[26:02] would get of kt But on the other hand,
[26:07] you know what the uh output VT should be
[26:13] uh based on um what the query times uh
[26:17] or based on uh what the
[26:19] Hang on one second. [laughter]
[26:21] I don't want to I don't want to get this
[26:29] you calculate KT with respect to the
[26:32] matrix. And you can view this matrix as
[26:38] a way of uh calculating the uh the way
[26:42] of calculating the mapping from a query
[26:45] to a value. And you can also get the the
[26:50] actual value and subtract out uh what
[26:53] the value you get when multiplying it
[26:54] from the previous uh together with the
[26:57] previous matrix is. And this is
[26:59] essentially the error uh that you get
[27:01] here. And then you want to reduce the
[27:04] error. And so in order to reduce this
[27:07] error, what you do is you um essentially
[27:12] add in this uh this term which is KT uh
[27:15] times the error term. And after you do
[27:17] this, if you multiply in KT to the new
[27:20] matrix, you will no longer have any
[27:23] error. But you don't want to make an
[27:25] update that is too big. So you add this
[27:27] beta term. This is essentially a
[27:28] learning, it's similar to a learning
[27:31] rate. And this learning rate will make
[27:34] the updates uh smaller. And so uh if you
[27:37] if you do this, this allows you to
[27:40] basically nudge the matrix in the
[27:44] direction of uh the in the direction
[27:48] that will cause a query that looks like
[27:50] the current key to output the value that
[27:53] you want essentially. So it's it's
[27:55] reducing the error uh reducing the error
[27:57] in the prediction of the value that you
[28:03] So um as I said this is going to be a
[28:05] little bit high level. Um the the papers
[28:08] are are pretty good uh descriptions of
[28:09] this.
[28:14] Um so after this um this basically what
[28:15] this is doing is this is pushing you in
[28:20] the direction of the uh of making the
[28:23] the matrix a better predictor of the uh
[28:27] the value. But one problem with this is
[28:29] you can build up lots and lots of
[28:32] context uh from the previous uh spots
[28:35] and linear attention doesn't have any
[28:38] mechanism to prevent very far away cont
[28:42] uh context from having a bad
[28:47] influence on your next predictions. And
[28:52] so if you have like a very weird key far
[28:54] back in the future, it might have a very
[28:57] big influence on you in the f uh in the
[29:01] future. And so the way they fix this is
[29:04] basically they have a decay term to make
[29:07] uh to make the
[29:10] matrix decay
[29:14] a little bit at every time step. And by
[29:16] decaying the matrix a little bit at
[29:17] every time step, they're basically
[29:20] discounting the the far in the past
[29:23] context. And so you multiply um the
[29:27] matrix by alpha t and then you add this
[29:31] uh st tilda into uh into your
[29:33] calculation here and update the matrix.
[29:35] And so the stronger you make this decay
[29:38] basically the the more quickly uh it
[29:41] will forget the previous context. And so
[29:43] you can make this more local or or less
[29:50] And so this is uh gated delta is used in
[29:53] the Quen models. So it's one of the more
[29:56] uh the more popular methods now. Um but
[30:00] both uh GLM and uh KI which are kind of
[30:02] two of the state-of-the-art models use a
[30:05] slightly more expressive version of this
[30:07] uh where they basically have a per
[30:10] element uh decay term. So each element
[30:13] can decay at a different speed. And uh
[30:14] because each element decays at a
[30:17] different speed, you can have some uh
[30:20] portions of the context that uh you know
[30:22] carry over very long time periods, some
[30:24] portions of the context that carry over
[30:33] Cool. So hopefully this was more or less
[30:37] uh more or less legible. Um
[30:39] any any questions here?
[30:41] Long long story short, it's basically a
[30:44] way to turn uh into
[30:48] um it's a way to turn
[30:50] the idea of attention to something that
[30:54] you can calculate um in context. Mamba
[30:57] is uh something that's very similar um
[30:59] but it's a little bit more
[31:02] mathematically involved um uh and I I
[31:04] decided to skip over it. uh I covered it
[31:07] more in the uh language model uh
[31:09] description course but similar idea but
[31:14] just a bit more complex uh in the math.
[31:15] So the next thing I'd like to talk about
[31:18] is sparse attention. And so sparse
[31:25] attention is uh basically looking up a
[31:27] not attending to everything in the
[31:30] previous context but only attending to
[31:32] some things in the previous context. And
[31:33] essentially you limit the number of
[31:35] things that you look up in the previous
[31:37] context. There's a few ways you can do
[31:41] it. Um originally in there was a sparse
[31:44] attention paper by OpenAI uh quite a
[31:46] while ago like 5 years ago or something
[31:50] like this. Um and basically uh what they
[31:53] did was they had sparse attention every
[31:57] you know uh 512 tokens or something like
[31:58] this. And what this does is it means
[32:01] that you still have a fixed it's still
[32:03] quadratic in the sequence length but
[32:06] it's 512 times less than if you attended
[32:08] to every token and that's like good
[32:10] enough uh that you can manage to
[32:12] calculate it over the context that
[32:14] you're interested in.
[32:17] Another option is to do um content
[32:19] dependent sparse attention. And
[32:21] basically what this does is you have a
[32:23] very cheap way of calculating attention.
[32:25] Like for example, you can down project
[32:27] the attention vectors to be very very
[32:30] small and then you do attention over
[32:33] these very very small uh attention
[32:35] vectors. You pick the top k ones and
[32:36] then you do full attention over the top
[32:40] k. So uh that's uh another way that you
[32:42] can do this
[32:43] and this is what's used in deepseek.
[32:43] Yeah.
[32:46] >> How do we define the metric for which we
[32:50] do the top similarity compared in this
[32:53] in the shrine space we just do like
[32:55] coine distance.
[32:57] >> Yeah.
[32:59] >> Yeah. I I think it's typically not
[33:03] cosine but it's just product but yeah
[33:05] >> I I I think although maybe maybe they're
[33:07] normalizing beforehand. They actually
[33:10] don't know that detail.
[33:13] Any other questions?
[33:17] So basically um these
[33:21] th this is a very very cheap way to
[33:23] achieve global attention because you can
[33:26] just uh write a kernel that will do this
[33:30] for you. Um this over here will uh
[33:32] require you to have two passes, but you
[33:35] know it's potentially uh more accurate.
[33:37] So um I I've seen both of these used
[33:44] So a final um a final thing is KV
[33:46] compression. How many people saw this in
[33:49] a language modeling course?
[33:53] Maybe some people. Okay. Um so I will uh
[33:57] I'll explain this. So basically um this
[34:00] is standard multi head attention. And so
[34:01] in standard multi-head attention, you
[34:04] have a bunch of heads and each one has
[34:08] values and keys and all of these are a
[34:09] certain dimension. So they're like
[34:12] dimension, let's say they're dimension D
[34:16] and you have uh you have like a certain
[34:20] number of heads. Let's say that's H. Um
[34:26] the two main ways that people solve uh
[34:29] or help uh this problem of having very
[34:33] uh large and expensive KV caches is uh
[34:35] grouped query attention. And grouped
[34:38] query attention basically uh just uses a
[34:42] smaller number than h um you usually h
[34:46] divided by some uh power of two uh
[34:50] number of uh keys and values. And
[34:52] because it's the KV cache, it's not the
[34:55] KVQ cache. Um
[34:57] if you reduce the number of uh keys and
[34:59] values that are used, you reduce the
[35:01] amount of memory that you need to hold
[35:02] the KV cache. This is really important
[35:06] because if it gets very large then um it
[35:08] limits the number you can fit on one GPU
[35:11] and so this can usually be reduced by
[35:13] like four or by eight or something like
[35:17] that. Um multiquery attention is just
[35:19] like grouped query attention with a
[35:21] single one. So you can kind of almost
[35:22] skip over that. You already know what it
[35:26] means. Um multi head latent attention
[35:30] the the um
[35:35] is essentially down projecting uh the
[35:39] size of the keys and values. So it's not
[35:40] reducing the number of heads, it's
[35:43] making each head smaller. And so this is
[35:45] similar to what I talked about with the
[35:47] top K attention. Um and of course you
[35:48] can combine both of these together as
[35:50] well. You could have group query
[35:52] attention with um you know smaller uh
[36:05] Okay, cool.
[36:07] Um so the these are the method the
[36:09] architectural methods that people use to
[36:13] handle very long contexts and with these
[36:16] um you can handle up to a million uh
[36:19] tokens. So like this is uh you know this
[36:22] makes the efficiency possible.
[36:25] The next thing is uh training long
[36:29] context models. And this is actually uh
[36:32] pretty hard. And the reason why is
[36:36] because um if we want something to
[36:41] handle 128k tokens or even more, there's
[36:44] actually not that much data on the
[36:48] internet that is 128k coherent tokens.
[36:51] Um it's actually a lot of a lot of data.
[36:53] it's more than most Wikipedia articles,
[36:55] you know, um you're starting to get in
[36:57] the in the order of like having a book
[36:59] uh that you need to have and there's not
[37:00] that many books on the internet. So,
[37:02] typically what you do is you start out
[37:05] with like short pre-training. Um you do
[37:07] more continued training with longer
[37:08] documents and then you do long
[37:10] adaptation.
[37:14] Um I wrote packed sequences here. Um,
[37:17] but packed sequences are are useful can
[37:19] be useful for efficiency, but they're
[37:20] not super useful for learning long
[37:24] contexts because um every time you like
[37:26] let's say you pack 10 documents into a
[37:28] sequence, you're not learning to attend
[37:30] across the documents and in fact you
[37:33] probably should not be. So um you really
[37:36] need coherent uh long sets of data to do
[37:43] Um so I'm going to talk about a few
[37:45] things that we do here. Um the first
[37:47] thing I'm going to talk about is uh
[37:51] handling positional encodings. Um so
[37:54] absolute positional encodings uh I I
[37:56] hope everybody has seen in their
[37:59] language modeling class. Um but
[38:03] basically uh each individual
[38:07] entry in the uh
[38:10] each individual word embedding uh gets a
[38:12] position vector and that position vector
[38:15] is typically calculated by uh some sort
[38:17] of function like using signs and
[38:19] cosiness and other stuff like this. So
[38:20] hopefully you know most people have seen
[38:23] this. So I'll I'll kind of skip over
[38:25] that. Also maybe most people have seen
[38:28] rope. Are people generally familiar with
[38:32] rope? Okay, I see a fair number of
[38:34] people. I see actually less people uh
[38:36] than I would have expected, but um uh
[38:39] maybe people are just uh not interested
[38:42] in raising your hand. Um [laughter] but
[38:46] uh but basically um rope rope is pretty
[38:48] elegant mathematically in my opinion. Uh
[38:50] basically the problem they were trying
[38:53] to solve is they wanted to have a
[38:58] positional embedding. um where the
[39:01] positional uh or positional encoding
[39:03] where the positional encoding is
[39:05] entirely
[39:08] determined by the relative distance uh
[39:10] between two tokens.
[39:13] And the
[39:16] reason why they wanted to do this is
[39:19] they didn't they didn't want the
[39:23] absolute position to have an effect on
[39:25] uh they didn't want the absolute
[39:27] position to have an effect on whether
[39:29] two tokens would attend to each other.
[39:33] And so
[39:36] this is this has been quite effective
[39:41] and a lot of uh a lot of models use
[39:44] rope. Um the the math I'm not going to
[39:45] go through here because it's kind of not
[39:47] the main point, but they do some
[39:49] interesting stuff with rotations and
[39:51] imaginary numbers and stuff like this.
[39:55] Um but there's also this like super
[39:57] counterintuitive
[39:59] uh nope.
[40:02] which is uh don't don't use positional
[40:06] encodings at all. Um and if you took
[40:09] your uh class on transformers
[40:12] uh you might have heard this scary stuff
[40:14] which is like you need positional
[40:17] encodings for transformers because
[40:21] otherwise something in position one in
[40:24] position five will have exactly the same
[40:27] representation. So if you have like this
[40:30] this is a cat but this is not a cat it
[40:31] will attend to both of the cats the same
[40:39] theoretically when the transformers were
[40:41] originally created um this might have
[40:43] been true but now actually it's it's not
[40:45] true anymore based on the transformers
[40:50] we use now. Um anybody have an idea
[40:51] why this is the case? I've kind of given
[40:55] a hint in the slide but
[40:56] you might also need to know a little bit
[40:59] of the history of transformers uh which
[41:00] is uh before we were using encoder
[41:03] decoder models uh where the encoders
[41:04] encoded all of the input and then the
[41:08] decoders uh generated the output any
[41:11] idea
[41:13] >> because we're doing causal masking
[41:16] exactly so um to elaborate on that a
[41:18] little bit if I go back to our
[41:25] Um, we have the keys um, and the
[41:30] queries. And if we look at the queries,
[41:32] even if you have cat at position two and
[41:35] cat at position five, the cat at
[41:36] position two is only attending to the
[41:39] previous token where the cat at position
[41:41] five is attending to the previous four
[41:45] tokens. Um, and so both of them are like
[41:47] actually different. um starting at least
[41:49] in the first layer of attention. And so
[41:52] you can tell like even if they are
[41:55] exactly the same word, the embeddings
[41:56] starting in the first layer of attention
[41:58] will will not be different. And there's
[42:01] kind of uh this counterintuitive paper
[42:03] that demonstrates that you don't need uh
[42:06] positional encodings at all. And this is
[42:10] especially true um this is in auto
[42:12] reggressive uh transformers. In non-auto
[42:14] reggressive transformers where you're
[42:15] attending all the tokens are attending
[42:17] to each other. You still do need
[42:21] positional encodings. Um
[42:22] this is especially true when we start
[42:25] talking about like gated delta because
[42:28] gated delta has like the decay term and
[42:30] uh other things like this which causes
[42:33] each uh token to be different. So once
[42:34] we start having those sort of local
[42:35] biases, we actually don't need
[42:39] positional uh encodings anymore.
[42:41] Um
[42:42] and
[42:46] if you uh if you look um
[42:51] we uh the first two here have rope uh or
[42:53] at least partial rope. The second two
[42:55] have nope uh no positional attend
[42:59] encodings. Um the the fourth one uh
[43:02] relies entirely on implicit order and
[43:05] mamba and some of them in uh and inkling
[43:08] has relative positional encodings. So
[43:09] you can see that it's kind of like half
[43:11] split between having relative positional
[43:14] encodings and not at all. But like let's
[43:16] say we did have positional encodings. Uh
[43:17] one thing you need to worry about for
[43:20] long context is uh position
[43:24] interpolation or position extension. And
[43:25] what this means is if you have a
[43:29] pre-training range, um, you need to
[43:31] essentially extend your model so that
[43:33] it's able to handle longer sequences.
[43:38] And so the the promise of rope was that
[43:41] rope relied only on the relative
[43:46] position uh between the different tokens
[43:49] in the output. But
[43:52] that that's fine as long as the relative
[43:56] position is only um well okay there
[43:58] there's two reasons why this is not
[44:00] fine. So number one if you're training
[44:02] on
[44:05] sequences of length L and then you
[44:09] extend to sequences uh of length SL then
[44:12] it's never seen two tokens attend to
[44:14] each other over a distance of more than
[44:17] L. So the tokens that are more than L
[44:19] away from each other are going to have
[44:20] problems attending to each other and
[44:22] you're not going to be able to uh manage
[44:26] that very well. Um the other problem is
[44:28] that actually relative positional
[44:31] encodings are only one part of the story
[44:32] and like actually the auto reggressive
[44:34] mask has an effect in all these other
[44:37] things. So you can't just take rope and
[44:39] expect it to work uh really well on
[44:41] longer sequences.
[44:45] And so the typical way you fix this is
[44:46] there's a parameter in rope that
[44:48] basically
[44:51] uh
[44:55] let me see if I have it in my slide.
[44:57] So I I don't I don't really have it in
[44:59] my slide, but there's basically a um a
[45:01] parameter in rope theta that uh tells
[45:03] you how much you rotate at each time
[45:08] step. and you divide this theta by the
[45:10] uh multiplier by which you extended the
[45:12] sequence. And so basically you're
[45:16] stretching the rope position so that the
[45:19] rope uh position at position zero would
[45:22] um or the rope position at position like
[45:26] five would be 5s uh would be equivalent
[45:28] to the position 5s in your uh extended
[45:30] context.
[45:34] And there's also um a more sophisticated
[45:37] way of doing this called yarn uh which
[45:41] basically is uh similar
[45:47] in spirit uh to like the delta uh the ki
[45:49] delta attention
[45:51] um which
[45:54] basically said that we want some of them
[45:55] to be very long distance and some of
[45:57] them to not be very long distance. In
[46:00] yarn essentially you have some of them
[46:03] be uh extended more and some of them be
[46:06] extended less and so you don't um you
[46:08] don't necessarily interpolate all of
[46:16] So um yeah in the interest of time I'm
[46:18] not going to go into like a lot of
[46:19] detail about this but basically these
[46:22] are um uh these are the various methods
[46:29] So, um,
[46:31] I'd like to talk a little bit now, um,
[46:33] taking a step back from the detailed
[46:35] modeling stuff and going into the data
[46:39] that you can use to train this. So, um,
[46:40] as I mentioned before, packed examples,
[46:42] you can just pack a whole bunch of stuff
[46:45] in there, um, a whole bunch of documents
[46:48] in into your context length. And this
[46:50] will work at training models to be able
[46:52] to process things near the end of your
[46:54] context window. But what it won't work
[46:58] for is the kind of global coherence. And
[47:01] um so there's a number of different ways
[47:03] that people do this. One way is just to
[47:07] find um very long documents uh like
[47:09] books or something like this. There
[47:11] aren't a lot of these uh but there are
[47:14] books. There are code bases and code
[47:15] bases tend to be coherent. So you can
[47:17] just download a big codebase and that
[47:20] will definitely have more tokens. Um
[47:23] multi-document corpora of some kind. So,
[47:25] you know, like uh you can get a whole
[47:26] bunch of documents that are on the same
[47:27] topic and then at least you'll have
[47:30] topical coherence between them. Um I've
[47:32] also seen people train on patents
[47:34] because patents have like there's lots
[47:37] of public data for them and you can kind
[47:39] of link link them together.
[47:41] A big source nowadays is agent
[47:45] trajectories because you know agents can
[47:47] make very very long trajectories if you
[47:48] just interact with them for a little
[47:51] while. So that's another one. And then
[47:53] you can also create synthetic tasks and
[47:55] a lot of the evaluations are synthetic
[48:03] Um and I I have some examples of how the
[48:05] models do this. Um a lot of the model
[48:07] training companies don't like to share
[48:09] these details with you because this is
[48:13] like if they release their um well so
[48:14] number one the closed models like
[48:18] anthropic open AAI you know those places
[48:20] uh uh Gemini they will not release even
[48:22] their architectural details the open
[48:23] model companies have to release their
[48:25] architectural details otherwise you
[48:27] can't run their model so what do they
[48:29] keep secret they keep their data mixes
[48:31] and their their training strategy secret
[48:34] so um this there's a lot less detailed
[48:38] stuff that we can say. Um, but there's
[48:41] uh all of them explain all of the ones
[48:42] in here explain a little bit about their
[48:45] data mixtures and they are things like
[48:47] uh cleaned up sampled documents and
[48:50] video um documents, repository files,
[48:53] issue, PRs, uh long document QA,
[48:56] scientific papers and technical reports.
[48:58] And then uh they also create a bunch of
[49:00] synthetic tasks. And typically they have
[49:03] a scaling strategy of like 8 64 256 1
[49:05] million uh that that sort of stuff as
[49:12] Oh yes. Um [clears throat]
[49:14] one other
[49:17] logistical detail that you might need to
[49:19] deal with um or might not need to deal
[49:20] with depending on the size of the model
[49:22] you're training. like for example for
[49:23] your project if you want to start
[49:27] dealing with um uh larger models is
[49:30] context parallelism and basically what
[49:34] this means is there's a bunch of uh ways
[49:36] to do parallelism when training models I
[49:38] wrote context parallelism up here what
[49:40] are two other ways uh that you can
[49:41] parallelize models during model training
[49:44] or serving
[49:50] >> data parallelism
[49:52] >> yeah you you said a more specific
[49:53] example of the second one but data
[49:55] parallelism and I would say model
[49:57] parallelism in general and model
[49:59] parallelism can have lots of varieties.
[50:02] It can have uh expert parallelism where
[50:03] you have different experts on different
[50:06] machines uh tensor more generally tensor
[50:10] parallelism where you split um uh the uh
[50:11] the parameters and you can also have
[50:12] pipeline parallelism where you have
[50:14] different layers on different uh
[50:16] different devices. But context
[50:18] parallelism starts becoming import more
[50:20] important for agents because when you
[50:22] train agents you want to train them on
[50:25] very long contexts. And so uh the way
[50:28] this works is you will compute like one
[50:31] part of the context uh the keys and
[50:32] values. So you send it to the next
[50:35] device calculate the keys and values for
[50:37] the next for that part send it to the
[50:42] next device uh and etc etc. So um this
[50:44] is uh very useful. It's really important
[50:47] if you start getting above like 32k
[50:51] 32k context or so. Um, but it's also a
[50:54] pain because
[51:00] um
[51:02] you have all the modeling people saying
[51:05] I want my I want my KI delta attention
[51:06] and then you have all the info people
[51:08] saying but wait I need to implement a
[51:10] context parallel kernel for KI delta
[51:12] attention and make sure it actually
[51:14] works and you can back prop through it
[51:19] and all of these other things. So um I I
[51:20] personally had an experience where I was
[51:24] trying to train uh Quen uh for uh like a
[51:29] smaller quen model like 135 uh 35b and
[51:32] uh I I wanted to go do use context
[51:33] parallelism on it and it's like there's
[51:35] no kernel for gated delta net anywhere
[51:38] on the internet and so um you need to uh
[51:39] you need to either go in and implement
[51:41] that kernel or decide to do something
[51:44] else. So um th those two can conflict
[51:46] some of the times. So be be aware I
[51:53] um the the good news is for like
[51:55] standard attention and sliding window
[51:56] attention and stuff like that all of
[51:59] those will have uh kernels more easily
[52:00] implemented. The hard parts are where
[52:02] you're like not doing a standard
[52:11] Okay. So the next part I'd like to talk
[52:14] about is prompt and KV caching. This is
[52:16] uh very important even if you're not the
[52:18] person who's implementing the language
[52:19] model, but also if you're just a person
[52:22] who's um
[52:26] like running agents uh yourself, but I'm
[52:28] going to talk about uh the the technical
[52:30] details of how it's implemented. So, you
[52:32] know, at least you you have a good uh
[52:35] idea about how that works. So um
[52:37] basically
[52:40] when we I I simplified this a little bit
[52:42] but when we're generating an agent call
[52:46] we have an input uh we have an output uh
[52:47] so this could be like the the messages
[52:49] and tool calls and then we have the tool
[52:59] as we calculate the input we do prefill
[53:02] and as we calculate the output uh we do
[53:04] uh basically decoding Right? And so
[53:06] during prefill and decoding, we have to
[53:08] calculate the KV cache. This is all done
[53:11] in a batch. Uh this is done every time
[53:13] we generate a token. But after we have
[53:16] that, we have the uh key and value uh
[53:18] for each of the positions up until the
[53:20] end of the output. And so what we can do
[53:22] is we can throw that in a cache and then
[53:24] we don't need to calculate it anymore.
[53:27] The tool result is new uh because you
[53:29] know we don't calculate over the tool
[53:31] result. So this becomes a new input and
[53:33] we generate an output and we get another
[53:37] tool result. And so in step two we need
[53:38] to calculate the KV cache over the new
[53:41] input and we uh during prefill and the
[53:44] output but we can reuse the cache
[53:45] and then we do that over and over and
[53:49] over again. And so as you imagine um as
[53:52] you can imagine I just showed steps 1 2
[53:55] 3 but by the time we get to step 50 if
[53:57] we haven't done anything tricky with our
[53:59] output this is going to be 50 times
[54:02] larger than the new input in the in the
[54:04] output right so that's pretty
[54:06] significant savings if we can cache this
[54:12] and here are some examples from actual
[54:15] papers uh that you know examine this and
[54:18] basically What we can see is this is
[54:20] like the the token length on uh
[54:25] different GPUs and this is the amount of
[54:28] uh of compute that you need with caching
[54:31] and no caching. And so the upper one of
[54:34] the same color is uh or the lower one
[54:36] with the same color is caching and the
[54:40] the upper one is no caching. So uh
[54:42] basically as the sequence gets longer
[54:44] the non-cashed one becomes quadratic and
[54:53] This also shows up in how much you pay
[54:56] to run an agent. And so I I pulled all
[54:58] of these numbers from uh the official
[55:01] pricing. And basically you can see here
[55:04] that if you go through all of these uh
[55:05] all of these numbers including the
[55:08] commercial ones typically cashed tokens
[55:10] are onetenth of the price of uncashed
[55:13] tokens. And so what this means is you
[55:16] need to be very aware of uh whether your
[55:18] tokens are being cached or not. Uh
[55:20] because if they're not being cached uh
[55:22] you're going to be paying a lot of money
[55:26] to be running your agents. Um,
[55:28] so does anyone have an idea of what a
[55:31] good uh cash hit rate is
[55:33] if you're running an agent? Yeah.
[55:34] >> 80 to 90%.
[55:49] >> Um, yeah. So I I heard 80 to 90% I heard
[55:53] like more than 95%. I my my impression
[55:56] is 90 to 95 is everything is fine. Like
[55:59] I'm I'm good with 90 to 95. If it's less
[56:01] than that, you might be fine, but you
[56:03] might be might be losing out somewhere.
[56:08] Um so, uh yeah, so basically you can you
[56:11] can cache most of your tokens. Um one
[56:12] other interesting thing is the output
[56:14] also tends to be five times more than
[56:17] the input. So um this is uh there's a
[56:19] 50x difference between output and cached
[56:22] input which just reflects the amount of
[56:25] uh uh the amount of cost uh savings that
[56:28] you can get from serving it.
[56:34] So why why is caching um so much cheaper
[56:36] is maybe kind of obvious. You just need
[56:42] to look up um you need to look up the
[56:44] outputs. uh you just need to look these
[56:46] up instead of like actually uh
[56:49] performing the calculation over them. Uh
[56:50] especially the feed forward network
[56:52] calculation is pretty expensive in
[56:54] transformers and so being able to skip
[56:58] that is is uh particularly a win. Um but
[57:02] how do we actually manage that? So
[57:06] um the first thing is uh how do you hold
[57:09] it in memory? And there's two like most
[57:12] popular open-source
[57:15] uh two most popular open-source
[57:18] LLM serving libraries VLM and SGLANG and
[57:22] both of them are based on an innovation
[57:26] around the how you manage KV caching. Um
[57:30] so VLM's main technical in innovation
[57:32] and like of course they have a lot more
[57:33] stuff in there now. They're like general
[57:35] purpose serving libraries, but like the
[57:38] main technical innovation that led to
[57:41] VLM was something called page detention.
[57:43] And basically the way it works is you
[57:46] have physical GPU memory blocks and you
[57:49] rear you arrange them like kind of
[57:53] memory blocks or or disk blocks on uh
[57:57] like more typical uh like CPUbased
[58:01] machines. And so you might have uh block
[58:04] zero uh block one block two that you
[58:07] actually need to calculate and they put
[58:10] that you know in like block one and then
[58:13] block seven and then block three or
[58:14] sorry uh block seven block one block
[58:18] three and then you have an index to each
[58:20] one of these uh as you're generating.
[58:22] And the reason why they wanted to do
[58:23] this is they want to be able to generate
[58:26] in parallel many sequences in parallel
[58:29] and when you finish generating um you
[58:31] can like evict that from your memory and
[58:34] so you can uh evict whole blocks at once
[58:36] and this makes the calculation more more
[58:39] efficient. So um this is uh one
[58:40] technical trick that they used to make
[58:43] this uh you know make parallel serving
[58:46] work.
[58:48] Um
[58:50] the technical innovation that kind of
[58:53] led to SG lang in particular uh was
[58:55] something called RAIX attention and this
[59:00] is specifically focused around uh like
[59:04] re reusing already cached uh out uh
[59:08] inputs. And so what they do is they form
[59:13] a a tree basically uh it's a radics tree
[59:15] and they use this to look up prefixes
[59:18] that have been used already. And so this
[59:20] uh when it first came out this was
[59:22] specifically focused around uh chat bots
[59:24] like chatgpt
[59:25] uh because you know you can have
[59:27] somebody start a conversation and then
[59:29] continue the conversation and so you'll
[59:31] be caching some portion of the already
[59:36] done conversation. But for uh now it's
[59:38] like much much more important for agents
[59:39] because agent conversations are much
[59:41] longer and much more frequent. So we
[59:50] Um so another uh another thing that you
[59:52] need to think about um which is handled
[59:55] in uh newer versions of sglang for
[59:57] instance is let's say you're doing
[01:00:00] multi-achine serving. So you're serving
[01:00:05] on um you know different machines uh you
[01:00:07] know maybe you have a data center with
[01:00:09] like 64 nodes or 128 nodes or something
[01:00:12] like this. um every time a request comes
[01:00:14] in, you want to route it to the machine
[01:00:17] that has your KV cache that has the best
[01:00:21] KV cache for you um to be accessing and
[01:00:23] so that you actually have cache aware
[01:00:25] routing uh route it to the appropriate
[01:00:27] place and then have the worker with the
[01:00:31] best uh KV cache match uh process set.
[01:00:33] And so
[01:00:36] I love getting all my uh my serving
[01:00:39] statistics from Open Router um because
[01:00:42] they have so much data and uh they cover
[01:00:44] all of the things I want to talk about,
[01:00:47] but I believe they even have
[01:00:50] a ranking of providers by cash hit rate.
[01:00:51] [laughter]
[01:00:54] I'm sorry mist the data the data doesn't
[01:00:58] lie but um you can see uh mistrol has
[01:01:02] the worst cache hit rate and then um you
[01:01:04] have other one other ones like Alibaba
[01:01:06] cloud or dicard or silicon flow that
[01:01:09] have higher cash hit rates um this is
[01:01:12] not entirely reflective of the provider
[01:01:13] being bad or something like that it
[01:01:15] could be just the workloads that they're
[01:01:17] running but there's a number of things
[01:01:20] that like actually factor into
[01:01:24] into this cache hit rate and um one of
[01:01:28] them one of them is how good is the cash
[01:01:30] routing. The other one is how fast is
[01:01:35] the cash eviction. Um so the providers
[01:01:38] will not hold your cash for you forever.
[01:01:42] Um they will uh you know evict your cash
[01:01:44] after a certain amount of time. Does
[01:01:47] anyone know how long this is for like
[01:01:49] popular providers? Have you ever taken a
[01:01:49] look at that
[01:01:52] >> yet?
[01:01:53] Close to an hour.
[01:01:56] >> Close to an hour. I I think the long
[01:01:59] like I'm not I'm not like super up to
[01:02:01] date on this, but I know anthropic used
[01:02:03] to be five minutes. And so it's
[01:02:05] basically if you have a an active
[01:02:07] conversation going on with them and you
[01:02:08] don't pause your conversation, you'll
[01:02:10] stay in the cache. Otherwise, if you
[01:02:11] like stop the conversation, you get
[01:02:14] evicted from the cache. I think you at
[01:02:16] least have an option to go up to an hour
[01:02:19] now. Um but I don't know if you um but
[01:02:20] like it costs a little bit more if you
[01:02:23] go up to an hour or something. Um but
[01:02:24] yeah, ba basically they don't want to
[01:02:26] keep this around because there this is a
[01:02:28] huge amount of memory uh that they're
[01:02:30] keeping in memory and so they want to
[01:02:32] use it if it's working and and evict it
[01:02:35] if it's not working. So um that that's
[01:02:36] another policy that could change your
[01:02:39] cash hit rate. The bad news for us as
[01:02:41] users is the pricing doesn't change no
[01:02:42] matter how good the provider is at
[01:02:47] routing or um or cash eviction. So you
[01:02:49] uh you might be paying just because they
[01:02:52] evict you uh evict you too quickly which
[01:02:54] seems a little bit unfair.
[01:02:57] >> Um yeah
[01:02:59] >> do they use like cash layering where you
[01:03:02] can store it on device in memory that's
[01:03:04] like adjusted to device and then on this
[01:03:06] >> yeah so the that's a great question. So
[01:03:08] the question was, do they use a cache
[01:03:10] layering where you have like a fast
[01:03:12] cache that's stored in the device and
[01:03:14] then uh a slower cache that's stored on
[01:03:17] disk or something like that? I actually
[01:03:18] don't know the answer to that question.
[01:03:20] That'd be a great uh like a great
[01:03:23] follow-up for us to do. Um the open
[01:03:25] source libraries also are probably not
[01:03:27] as sophisticated as the closed libraries
[01:03:29] because um if you look at all the people
[01:03:32] on open router their job is to be really
[01:03:35] good at serving and so you know they're
[01:03:37] some of them might be using open source
[01:03:38] libraries but they'll be building stuff
[01:03:40] on top of them and that's kind of their
[01:03:43] you know competitive differentiation. So
[01:03:47] um like I I think
[01:03:48] the internal solutions that inference
[01:03:50] providers are likely to be you know a
[01:03:51] bit better than the ones that are
[01:03:53] available in open source too with
[01:03:54] respect to that.
[01:03:57] >> They usually offload to CPU from GPU.
[01:04:00] Yeah.
[01:04:03] >> Yeah. Because your GPU memory is so
[01:04:12] >> Cool. Um so uh yeah. Oh, sorry. I
[01:04:14] skipped a important part. So, what does
[01:04:16] this mean? If you're just designing a
[01:04:18] harness and you're not deploying models
[01:04:21] or or anything like this, it means you
[01:04:24] need to be super super careful to not
[01:04:27] break your cache unintentionally.
[01:04:29] So, remember that your cache only works
[01:04:31] if the entire prefix is exactly the
[01:04:36] same. And so there's a bunch of things
[01:04:38] that we've thought about
[01:04:42] uh doing but we decided are a very bad
[01:04:44] idea because we don't want to break the
[01:04:48] cache. So one thing that's completely
[01:04:51] forbidden you should not do is don't
[01:04:55] change the system message every time you
[01:04:58] uh you take a step because that means
[01:05:00] like no caching essentially. uh you
[01:05:01] don't have a single message that you're
[01:05:04] able to cache. So one thing one very
[01:05:06] logical thing that you might think of is
[01:05:08] okay I want to append the current time
[01:05:11] and date to the system message uh so
[01:05:13] that the agent knows what time it is. Do
[01:05:15] not do this because the time and date
[01:05:18] changes every step and so that will
[01:05:20] break your cache. So if you do need to
[01:05:22] append it, append it to the final user
[01:05:25] message uh or the final uh tool call
[01:05:31] result that you get. um and uh like
[01:05:34] changing your um changing your tools uh
[01:05:36] dynamically in the middle of the
[01:05:37] conversation. You can do this. That's
[01:05:41] okay. Um another thing is a very logical
[01:05:43] thing that you might think of doing is
[01:05:45] routing to a different model every time
[01:05:47] you uh every time you take a step. So
[01:05:49] it's like this step looks like a really
[01:05:51] good model for you know a really power a
[01:05:53] really good step for a really powerful
[01:05:57] model. um like uh like I want to do this
[01:05:59] step on Fable and then I want to do the
[01:06:02] ne next three steps on um on a cheaper
[01:06:04] model to save money. But the thing is
[01:06:07] you're still paying
[01:06:09] you're still paying the you know 10x
[01:06:12] cost for Fable the next time you use uh
[01:06:16] Fable. So you really need to be very uh
[01:06:18] frugal in the amount of switching you're
[01:06:19] going to be doing if you want to be
[01:06:20] doing switching to save cost for
[01:06:26] Cool. Um,
[01:06:28] so the final thing I'd like to talk
[01:06:31] about is context compaction. Um, how
[01:06:33] many people know know about this? Use
[01:06:37] this in your everyday coding agent use.
[01:06:39] How many people are really excited when
[01:06:42] it says compacting context?
[01:06:43] [laughter]
[01:06:48] That's nobody good. So um the the basic
[01:06:51] idea behind context compaction is uh
[01:06:55] that you have uh before
[01:06:58] and uh this is you know all your
[01:06:59] observations and actions that you might
[01:07:03] have had. Um then after what you tend to
[01:07:05] do is you tend to take your previous
[01:07:09] context and you crush it down into just
[01:07:12] the essence of the previous context. Um,
[01:07:17] and so the reason why people are
[01:07:19] like not excited about using this, uh,
[01:07:21] perhaps obviously is if you do a bad job
[01:07:24] at this, your agent forgets things. It
[01:07:25] starts doing something completely
[01:07:28] different and, uh, maybe deletes your
[01:07:30] file system.
[01:07:33] So
[01:07:36] um we can view compaction as essentially
[01:07:39] trying to come up with a previous
[01:07:42] representation where your future action
[01:07:45] sequence um you take your history, you
[01:07:48] compact that, you get a working state
[01:07:50] and you want your future action sequence
[01:07:53] to be the same or you know similar or
[01:07:57] possibly better um if uh after
[01:08:01] compaction than it was before. Um
[01:08:03] at the same time you also have a
[01:08:06] constraint which your
[01:08:08] state needs to be bounded. So it needs
[01:08:10] to be small enough that you're happy to
[01:08:13] continue work.
[01:08:17] Um so if we look at what survives uh
[01:08:22] compaction um there's different ways of
[01:08:23] doing this. I'm going to cover the
[01:08:28] different ways that people do this, but
[01:08:32] a common strategy is to take some
[01:08:35] anchors and these can be the very first
[01:08:38] um like the very first things the user
[01:08:39] said when they started the session for
[01:08:42] instance. Um,
[01:08:44] so, uh, one of the answers to the things
[01:08:47] that I heard agents forget when I asked
[01:08:50] the question, what do agents forget was
[01:08:52] sometimes they forget the things at the
[01:08:55] very beginning of the session? And
[01:08:57] that actually might be a design bug in
[01:09:01] the agent harness that you're using. Um,
[01:09:03] because uh, some good agent harnesses
[01:09:06] uh, like kind of intentionally avoid
[01:09:07] deleting the stuff at the very beginning
[01:09:08] of the session because they think it's
[01:09:12] more important. Um, but it could also
[01:09:14] be, you know, impossible to avoid
[01:09:17] depending on the situation. Um, also you
[01:09:18] want the stuff in the middle that's
[01:09:21] encoded and put back into the context.
[01:09:24] And then the recent tail is often kept
[01:09:26] around. So often people will keep around
[01:09:29] the the most recent actions.
[01:09:31] Separately from this, I don't see this a
[01:09:35] whole lot, but um, you can also add the
[01:09:37] evidence to an evidence store. Actually,
[01:09:40] no, sorry. I I'll correct this. Um, the
[01:09:42] evidence is typically added to an
[01:09:45] evidence store. Um, and at the very
[01:09:47] least, if you're using a CLI coding
[01:09:49] agent, usually your full history is
[01:09:52] saved on disk somewhere. And so, if you
[01:09:54] know where on disk, your coding agent
[01:09:57] has saved all of this history. Even if
[01:09:58] you lose stuff through compaction, you
[01:10:00] can tell the coding agent to go back and
[01:10:01] read the history, and it can, you know,
[01:10:03] uh, read the history for you and find
[01:10:06] the the previous results. Um but there
[01:10:09] there are also uh possibly more
[01:10:11] structured ways of doing this and so
[01:10:13] then um you know other things can be
[01:10:15] discarded.
[01:10:19] Um so there's a few ways to decide uh
[01:10:21] compaction policy. Um the first one is
[01:10:24] the trigger and there's
[01:10:27] um
[01:10:29] essentially two ways of doing this. Um
[01:10:35] one is a token threshold. So you limit
[01:10:37] uh the token threshold. Uh so you can
[01:10:39] say I'm I'm only going to use up to 200k
[01:10:42] tokens. Once I go over 200k tokens, I'm
[01:10:45] I'm going to compact the context.
[01:10:47] Another thing is um like when you get
[01:10:50] forced to do that by the provider. Um so
[01:10:51] that's kind of like a hard limit on the
[01:10:53] number of tokens you can have. Um
[01:10:55] finally, you can also have a manual
[01:10:58] request. And so uh a lot of uh kind of
[01:11:00] coding agent toolkits for instance have
[01:11:02] a slashcompact
[01:11:05] uh like command that you can use to
[01:11:11] Um then based on that uh you'll select
[01:11:12] you might protect the beginning and keep
[01:11:14] the recent tail and compact the older
[01:11:17] region. Um replace it with a summary. Um
[01:11:19] that summary can be a structured
[01:11:23] summary. So sometimes uh they require a
[01:11:25] tool call uh that says this and this and
[01:11:27] this and this must be in the compaction
[01:11:30] summary. Sometimes it's just free text.
[01:11:34] Um there's also uh
[01:11:36] I think this is only open AI uh
[01:11:38] possibly. But basically they um they
[01:11:41] compact into
[01:11:43] something encrypted uh that you cannot
[01:11:45] read. So you can't see how they're
[01:11:46] compacting because they don't want you
[01:11:48] to steal their uh their precious
[01:11:51] compaction algorithm. Uh so uh so
[01:11:53] there's that.
[01:11:57] Um and then uh yeah, you can you can
[01:11:59] keep on on working on that.
[01:12:01] Um
[01:12:03] so
[01:12:06] one of the risks here is uh sometimes
[01:12:08] you can compact over and over and over
[01:12:10] again and the first time it works uh but
[01:12:14] as you walk through more um you uh you
[01:12:16] end up losing more and more. So again
[01:12:18] this is one of the reasons why people
[01:12:19] don't like compaction because it can
[01:12:22] cause the agent to go off the rails.
[01:12:26] Um so uh ba basically the way we
[01:12:28] evaluate this is typically in a holistic
[01:12:30] state. So you can vary the compaction
[01:12:32] algorithm and evaluate it against
[01:12:33] whatever benchmarks you're evaluating
[01:12:37] against. I would like to warn you uh
[01:12:39] about this. I have a a kind of like
[01:12:41] story from when we were first developing
[01:12:45] open hands which is um we actually I
[01:12:48] think made one of the first like
[01:12:51] production grade uh compaction
[01:12:53] algorithms. We called it compression
[01:12:56] then um and we evaluated it against
[01:12:58] bbench which is a very common you know
[01:13:01] benchmark for for coding agents and we
[01:13:03] worked pretty hard on it like as a
[01:13:04] research project for about a month or
[01:13:06] something like that and we were like we
[01:13:08] found this great compaction strategy. It
[01:13:09] doesn't reduce our score at all. it's
[01:13:12] saving us a lot of tokens. And then we
[01:13:15] actually tried it in our um we tried it
[01:13:18] in our our system and it made these
[01:13:21] really silly mistakes like um sending a
[01:13:24] pull request every time it compacted. So
[01:13:25] it forgot that it had sent a pull
[01:13:29] request to GitHub. And so uh you know we
[01:13:30] would get five pull requests for the
[01:13:33] same functionality because it had
[01:13:36] forgotten. Um or you know it would
[01:13:38] forget
[01:13:42] user instructions that were sent in the
[01:13:44] middle of the conversation because we
[01:13:46] had only evaluated on single turn
[01:13:48] conversations that had a single user
[01:13:50] message and we were compacting away the
[01:13:53] multiple user messages. So it's not just
[01:13:55] good enough to benchmark uh unless you
[01:13:57] have really really robust benchmarks
[01:13:59] that represent every use case. You kind
[01:14:00] of need to test them in the wild as
[01:14:03] well.
[01:14:05] Cool. Um so we're we're getting close to
[01:14:08] time. Uh but yeah, basically uh what I
[01:14:10] covered today is uh you know agent loops
[01:14:13] grow very quickly. Uh we have a lot of
[01:14:16] inference challenges in doing so. uh we
[01:14:18] can handle uh efficiency problems
[01:14:22] through architectures and um and caching
[01:14:24] and uh compaction is kind of the way we
[01:14:27] handle this uh once we expand beyond the
[01:14:31] level that we can handle. So um that's
[01:14:34] all I have. Uh if there is any questions
[01:14:36] happy to happy to cover them and next
[01:14:37] time we're going to be talking about
[01:14:39] skills and memory. So this is like even
[01:14:42] longer context over your entire uh your
[01:14:44] entire time. Um, are there any questions
[01:14:48] before we all uh all leave or
[01:14:55] >> Yeah, great question. Um, the question
[01:14:57] was, do we consider sub agents as a way
[01:14:59] to manage context? And yes, but we're
[01:15:00] going to talk about sub aents later, so
