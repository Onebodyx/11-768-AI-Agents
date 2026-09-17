# CMU AI Agents 2026: 1. What are Agents and How Do They Work?

- Видео: https://www.youtube.com/watch?v=UwfjzyLnvMg
- Длительность: 1:07:52
- Дата публикации: 20260908

## Расшифровка

[00:05] Okay. Um, hi everyone. Welcome to 11768,
[00:07] uh, AI agents. We're very excited to be
[00:11] teaching this new course, uh, which is
[00:13] timely as, uh, a lot of people are
[00:16] starting to use agents. Um, my name is
[00:18] Graham Nubig. I'm an associate professor
[00:20] in the school of computer science here.
[00:23] I've been working on agents for maybe
[00:25] uh, several years now. Uh, coding
[00:26] agents, web browsing agents, uh, those
[00:29] sorts of things. and I'll be co-eing
[00:31] together with Daniel who will be kicking
[00:34] off this class. So without further ado,
[00:36] I'll turn it over to him and he can
[00:38] start uh this and I'll I'll do the
[00:40] second part of the class.
[00:42] >> Thanks Graeme.
[00:45] How's this?
[00:48] Cool. Yeah. So um hi everyone. Really
[00:49] excited that you're here. My name is
[00:52] Daniel Freed. Um my research group also
[00:55] works on agents. Um so uh grounded
[00:57] agents and also interaction between
[00:59] people and agents and these days
[01:02] interaction between agent systems. So uh
[01:04] excited to talk about um all these
[01:07] topics with you and um yeah we have a
[01:09] really great core staff too who we will
[01:13] introduce in in a few slides. But yeah
[01:15] so agents are are really timely right
[01:18] now and um the capabilities of agents
[01:20] are advancing pretty quickly. So
[01:22] probably a lot of you are using coding
[01:25] agents in your you know day-to-day work
[01:28] and we've seen some big success cases of
[01:31] agents. So um one example is there was
[01:36] this uh nice experiment um by um Carlini
[01:39] at anthropic that
[01:42] saw could we develop a really complex
[01:45] piece of software using um a multi- aent
[01:47] uh configuration of a a recent coding
[01:50] model. And this was pretty successful.
[01:53] So 16 agents collaborated together over
[01:56] two weeks and constructed a rustbased C
[01:58] compiler which was able to compile the
[02:01] Linux kernel. And you've probably you
[02:02] know been using agents effectively in
[02:04] your own work and and seen how much
[02:05] better they've gotten especially in the
[02:08] last like year or so. There's
[02:11] limitations of current agents too. So
[02:14] how many folks have uh tried uh using an
[02:16] agent that controls your computer like
[02:18] controls applications or Okay. So, a lot
[02:20] of folks have How many uh folks have
[02:22] used OpenClaw?
[02:24] Yeah. So, we have a number of folks,
[02:26] too. Um, there was this pretty
[02:29] high-profile incident involving OpenClaw
[02:31] um which got posted on Twitter by the
[02:34] the person who ran into this where she
[02:36] was asking the model to organize her
[02:39] inbox and the model kind of went out of
[02:42] control and started deleting old emails.
[02:44] And uh so she's trying to intervene. She
[02:46] says, "What's going on? Can you describe
[02:47] what you're doing?" But the model says,
[02:49] "I'm taking the nuclear option. I'm
[02:51] going to trash everything in the inbox
[02:53] that isn't already in my keep list." And
[02:54] the user is trying to intervene, saying,
[02:57] you know, do not do that. Um, but the
[02:59] model goes on to delete a lot of this
[03:02] really valuable information. And at the
[03:05] end, it acknowledges uh that, you know,
[03:07] I learned my lesson. I'm not going to do
[03:09] this in the future. And I do remember
[03:11] that she told me this, um, but I
[03:13] violated it. So, what happened behind
[03:16] the scenes here? Well, it seems that it
[03:18] was the model compacted its past
[03:20] context, which is a way that we'll cover
[03:23] in this class of uh of reducing the past
[03:25] history so that the model is able to
[03:28] take in more um interactions with the
[03:29] environment, but that caused it to lose
[03:33] this instruction to not delete emails.
[03:35] So, models are getting much more
[03:37] capable, but they also still have really
[03:38] rough edges. And a lot of this class is
[03:40] going to be about how do you develop
[03:42] these capabilities and models starting
[03:44] from base language models but also what
[03:46] are the research problems and what are
[03:49] the remaining gaps that we need to fill.
[03:52] So let's just uh try to get a sense of
[03:54] what people think agents are are good at
[03:56] these days. So we have like six
[03:58] different tasks that you might want to
[04:00] try to use an agent for. And these are
[04:02] pretty subjective. I just want to get a
[04:03] sense of like what might you be
[04:05] comfortable with. Um, so let's do a show
[04:08] of hands for a task like say you have an
[04:11] online store like some uh code
[04:13] application that hosts a store for you
[04:14] and it started failing. You want to use
[04:17] an agent to try to diagnose that. How
[04:19] many people would be comfortable with
[04:21] having an agent carry this task out like
[04:23] fully on its own? Can we get a show of
[04:28] hands? Okay. Yeah. Um, how about having
[04:31] the agent like ask first as it's
[04:32] carrying out this task? Maybe asking you
[04:34] for help. How many people think that
[04:37] might be necessary?
[04:39] Okay. And how many folks think that this
[04:40] would just not be something that you
[04:42] would ever want an agent to touch at
[04:43] all?
[04:45] Okay. So, for this one, I think we had
[04:47] more autonomous.
[04:50] How about drafting and sending a product
[04:52] launch email to 50,000 customers? So,
[04:54] how many people are okay with this being
[04:56] fully autonomous?
[04:59] Okay, we got some brave souls. Um, how
[05:01] about asking first?
[05:04] Okay. And how about an agent shouldn't
[05:06] do this at all. I want to be responsible
[05:08] for it. Okay, so I think this one was
[05:11] was asked first. How about um collecting
[05:14] your tax forms and preparing and filing
[05:19] your 2025 tax return? Fully autonomous.
[05:22] Okay. Yeah.
[05:25] How about ask first?
[05:27] And how about never?
[05:29] Okay. Yeah. So I think this had the most
[05:32] never of anybody but ask first probably
[05:35] one migrating a payments API from Python
[05:38] to Rust. Say maybe you have some test
[05:40] cases that were written for the
[05:42] application in Python that you can apply
[05:44] to the Rust version. How many people
[05:45] would be okay with this being
[05:47] autonomous?
[05:50] Okay, how about ask first?
[05:52] Yeah, that was very close. I don't know
[05:56] which one was more and never.
[05:59] Okay. So, we'll uh let's uh have this be
[06:01] one for the agents. Autonomous. Buy
[06:03] concert tickets to my favorite band if
[06:06] they set up a show in an area in my
[06:09] area. Autonomous.
[06:10] So, you'd be okay with the agent buying
[06:13] the tickets, too, if it finds good ones.
[06:15] I think that one probably won. And how
[06:16] about this last one? Adjusting an
[06:19] insulin dose after a week of glucose
[06:21] readings. So, an agent like, you know,
[06:24] has all the like the capabilities to do
[06:26] this. Like if you're feeding it your
[06:28] health information, um it could monitor
[06:30] that. If you give it access to like
[06:32] something that can change a prescribed
[06:34] dosage, it could do that too. How many
[06:35] people would be comfortable with this
[06:38] autonomously?
[06:41] Okay, asking first.
[06:44] And how about never? Okay, so yeah, so
[06:45] that one was never, although I was
[06:48] thinking maybe it would be ask first. So
[06:50] cool. So I think you're all you all kind
[06:52] of have a sense of some of the
[06:54] boundaries that agents have. Although
[06:56] you know there's a lot of these tasks
[06:59] where we might just not be sure. Um but
[07:00] you also have a sense that like trust is
[07:03] important and later on in the class when
[07:06] we talk about like sandboxing and um
[07:08] security and um interaction and
[07:10] oversight by people um we'll get into
[07:17] Okay. So just to give like a very brief
[07:20] kind of uh tour of how agents have
[07:22] extremely brief. It's just two slides.
[07:23] how agents have progressed over the past
[07:26] few years. Um, and also to motivate some
[07:27] of the things that we'll see later on in
[07:30] the course. Um, so we've been doing some
[07:32] work on guey agents, like agents that
[07:34] can use computer applications here at
[07:36] CMU over the past few years. This is
[07:40] work from a lot of um, faculty. Um, and
[07:42] um, here's a demo that was made by um,
[07:45] one of our students, JY Co, um, two
[07:47] years ago showing an agent in action
[07:50] controlling the browser.
[07:51] And so you give it a task like navigate
[07:53] to the page of a good Thai restaurant in
[07:55] Pittsburgh. It should have at least 200
[07:58] reviews and 4.3 stars. And on the right
[07:59] here you can see, sorry it's a little
[08:01] fuzzy, but you can see the interactions
[08:03] with the language model like the chains
[08:04] of thought that are being produced. And
[08:06] on the left here, the model is
[08:09] controlling the browser um typing in the
[08:11] search box on Yelp and then navigating
[08:13] to this page. Fusidities is a really
[08:15] good Thai restaurant. Um and so that's a
[08:19] success and we've seen um you know
[08:20] frameworks and agents like this really
[08:22] taking off over the past few years with
[08:26] like um Manis and um OpenAI's operator
[08:29] cloud computer use agent and so on.
[08:31] And we've also done a lot of work uh
[08:34] here at CMU on building coding agents.
[08:36] Um uh Graham's group in particular has
[08:39] done a lot on this and also um through
[08:41] open hands which develops um open-
[08:44] source um agents. Um and uh here's a
[08:47] demo video uh from Graham which I'll uh
[08:50] play showing the agent like both writing
[08:52] code um but then also interacting with
[08:54] the application that it's built in the
[08:55] browser to test it out.
[09:02] >> So this will take a little while for the
[09:05] agent to work. Um, we can watch it work
[09:08] over here and see that it has uh made a
[09:12] directory for static files and templates
[09:15] and it has created the main app file. We
[09:17] can look at the changes it made to the
[09:19] app file uh by clicking over here in the
[09:21] changes tab which shows us all of the
[09:23] things it implemented. So that's kind of
[09:25] nice feature. So you can kind of watch
[09:27] uh what the agent is doing while it's
[09:29] working. and it's [music] editing the
[09:31] index file, the style file to make the
[09:34] app look nice.
[09:36] Uh requirements.ext to make it easy to
[09:39] install and adding a read me. So you can
[09:41] see it's kind of following good uh
[09:44] coding practices. And now it will start
[09:47] up the app. [music] And so it's running
[09:50] uh very very quick. And what I can say
[09:55] is let's run in the background
[09:58] and then [music] test out with your
[10:04] And so if I do this, it will uh run the
[10:09] [music]
[10:10] And it checked if the app is running.
[10:12] And now it should navigate there with
[10:22] uh it's checking the log and saw the
[10:24] port was already in use and it's trying
[10:26] it out. So that that's kind of the nice
[10:27] thing of agents. They can debug their
[10:30] own problems and uh and
[10:32] make sure that things work. So, okay, it
[10:42] And you see it browsed to the app. And
[10:44] we can see our tuning list app over
[10:48] here. And it sees that it's running, but
[10:50] now it wants to test the functionality.
[10:52] So, what we can do is we can see that it
[10:55] uh went through and it filled in uh buy
[10:57] groceries and it clicked. And you can
[11:00] see that uh in real time it's testing
[11:03] out your app and then it also is uh
[11:05] testing the delete functionality and
[11:07] other stuff like this. So I find this
[11:08] really exciting. I'm not, you know, the
[11:11] best front-end developer, but it's able
[11:12] to kind of [music] try out the front
[11:15] end, see if the functionality is working
[11:18] and fix any issues on the fly. And I
[11:20] even had one time where the app crashed
[11:22] and the agent realized that the app
[11:24] crashed even before I did and it was
[11:26] able to go in and fix the problems.
[11:28] So this is as simple as just saying, you
[11:30] know, go and develop an app and then
[11:32] test out if it works and you don't
[11:34] really need to do anything else. So now
[11:36] we're done. Uh let me stop this. In a
[11:38] real scenario, what I would do next is
[11:42] I'd ask it to push it to GitHub and uh
[11:43] you know finish it up so that I can
[11:46] continue working on it.
[11:48] >> Yeah. So we're excited to give you
[11:50] hands-on experience building agents um
[11:52] in this class. And in one of the
[11:54] lectures later on in the course, we'll
[11:58] cover open hands and its um SDK and how
[12:01] you can um uh develop agents of your own
[12:03] like this.
[12:06] So we um have a really great core staff.
[12:09] We have uh our our core staff all does
[12:12] research in these areas. um wrote some
[12:15] of the foundational papers and uh we'd
[12:17] love to have you all come up uh and uh
[12:21] introduce yourselves and um at the end
[12:23] of the course you'll be getting to work
[12:25] on a mini research project of your own
[12:29] and um we'll be uh getting guidance from
[12:31] the entire core staff um helping you out
[12:34] with that. So um yeah, if we can just uh
[12:36] go through and have each of you maybe
[12:38] just project uh and introduce
[12:39] yourselves.
[12:41] >> Yeah. So the yeah say it so the people
[12:44] in the back can hear like what what your
[12:46] research is on because uh then the
[12:49] people here can like essentially know
[12:50] what you're working on so they know
[12:51] which TA to talk to when you're working
[12:53] on like a project in that area for
[12:54] instance.
[12:55] >> Yeah.
[12:58] >> Hey everyone I'm a third year PhD
[13:01] student. I'm advised by Grant and Kamar.
[13:04] Um my research areas are focused on
[13:06] training agents to better leverage
[13:08] interest and compute and also organized
[13:11] in multi- aent systems.
[13:14] >> Hi everyone. Uh my name is Adita. I'm a
[13:16] first year Ph student uh working in the
[13:19] professor program. Uh my main research
[13:20] interests are like designing reward
[13:22] functions for like agent reinforcement
[13:24] learning. I particularly work on code
[13:27] generation for for now.
[13:31] Um hi everyone my name is and I'm a
[13:34] second year PhD student working with
[13:37] professor Anna Yeah and my current
[13:39] research focus is [clears throat]
[13:41] learning and
[13:44] research
[13:47] >> hi everyone I'm
[13:51] here working with the previous of
[13:54] working on mobility agents and
[13:58] recently I've been working on
[14:01] Hey uh I'm Sus. I'm a PhD student
[14:03] working with Daniel. Uh I work on how we
[14:05] can train agents to communicate more
[14:07] efficiently with people.
[14:09] >> Hi, I'm Lily. I'm a Syria business
[14:13] student by EMU. So I'm work on training
[14:15] on agents on authorizing coffee and
[14:18] battery.
[14:20] >> Uh hey everyone, I'm Andy. I'm a fourth
[14:23] year PhD. I work with Daniel and Monop.
[14:25] Uh I mainly work on alignment post
[14:26] training and also multi-agent
[14:28] introductions.
[14:37] >> Yeah. So uh like Graham said, we
[14:38] definitely encourage you as you're
[14:40] starting to think about your projects
[14:42] later on in the course, uh we'll talk
[14:43] about the course structure towards the
[14:45] end, but as you're starting to think
[14:46] about the projects that you want to do,
[14:47] TAS are going to be a really great
[14:49] resource for you to go to in office
[14:52] hours and get their expertise.
[14:55] So, we're also really grateful to um uh
[14:57] several really awesome startups for uh
[14:59] donating uh compute which you will be
[15:01] able to use in the assignments and
[15:04] projects for the course. Um and uh
[15:06] without their support uh we wouldn't be
[15:09] able to run um this at the scale that we
[15:10] would like to. So, we're really grateful
[15:14] to fireworks AI to modal um to prime
[15:17] intellect and to sale for uh helping to
[15:24] Okay. So today we'll give a brief
[15:27] overview of what an agent is and um then
[15:30] we'll talk about uh the plan for the
[15:33] class and how things will be structured.
[15:37] So an agent um agents have been around
[15:39] for a long time. The concept of an agent
[15:41] and um work developing agentive
[15:44] capabilities um isn't just you know a
[15:46] two or three year old thing. So, uh,
[15:49] Russell and Norvig in their foundational
[15:53] textbook on AI, um, define an agent as
[15:54] anything that can be viewed as, uh,
[15:57] perceiving its environment and acting
[15:59] upon that environment. And that's really
[16:01] true for the agents that we have now.
[16:03] And um, a lot of the techniques that
[16:05] were developed for agents in the past,
[16:07] not all, but a lot of them will apply to
[16:09] current agents too, especially things
[16:13] like search reinforcement learning. So,
[16:15] uh, how does this pan out for our
[16:17] current agents? So, agents are going to
[16:19] be situated in an environment, which
[16:20] could be something like a code
[16:23] repository, a website, um, some other
[16:26] application on your computer, and
[16:28] they'll be interacting with that
[16:30] environment by getting observations of
[16:33] the current state that they're in in the
[16:36] environment. So that's something like
[16:38] messages from the user they're
[16:40] interacting with, the contents of a file
[16:43] that they're um investigating, the
[16:44] current web page that they're on,
[16:47] screenshots, or as we'll focus on in a
[16:51] few slides, the results of um tools
[16:53] which are you like programmatic
[16:55] functions that they can execute in the
[16:58] environment to interact with it.
[17:01] And they're taking actions at each point
[17:03] in time. um which is going to these
[17:05] actions will update the environment and
[17:07] then change the state that the agent is
[17:09] in. So that could be something like
[17:12] replying to the user or editing a file
[17:14] or running a command in the shell or
[17:16] calling an API that backs the web pages
[17:19] that they're interacting with.
[17:21] And finally, there's also this notion of
[17:24] reward. So how do we define whether the
[17:26] agent was successful or not using a
[17:29] numeric score? And we could define this
[17:31] as like if there are some test cases for
[17:34] a codebase, do those pass? If they do,
[17:36] then you get a one, otherwise you get a
[17:39] zero. Uh for other tasks, it can be
[17:41] difficult to like have sort of a
[17:43] programmatic reward. So we might need to
[17:47] rely on an LLM as a judge to uh evaluate
[17:49] whether this was successful or not. In
[17:50] your second assignment, you'll be
[17:52] developing LLM as a judge based
[17:56] evaluation approaches among other eval.
[17:57] And maybe we're ultimately interested in
[17:59] did we, you know, make the user happy
[18:01] with the task that they asked the agent
[18:02] to do. So we could also use feedback
[18:05] from the user for that. And I think in
[18:07] our uh human interaction lecture that
[18:09] Valerie Chen is going to be giving a
[18:11] guest lecture later on, we'll talk about
[18:14] this.
[18:16] So we asked all of you to have prior
[18:19] experience training language models and
[18:21] um given that experience you should all
[18:24] be familiar with um language models um
[18:27] doing next token prediction right so at
[18:29] each step um the agent is going to
[18:30] predict a distribution over the next
[18:34] token um we'll sample or in some other
[18:36] way choose one of those tokens from that
[18:39] distribution um insert it into the
[18:41] context window of the model and repeat
[18:44] this um over over and over again. And
[18:48] recently we've uh seen a lot of a lot of
[18:51] improvements on uh complex reasoning
[18:53] tasks by introducing chain of thought to
[18:57] these models. So as um as you should
[18:59] remember a chain of thought is um
[19:02] predicting a sequence of tokens um which
[19:03] aren't the final answer that we want the
[19:06] model to output but do allow it to um
[19:09] sort of have a scratch pad um for its
[19:12] intermediate uh reasoning steps which it
[19:15] can then um use um and condition on to
[19:19] predict the final answer. And so this is
[19:20] like a non-aggentive setting, right?
[19:23] This is just the agent um interacting
[19:26] with prompts that you give to it. So how
[19:28] do we go from this to um having models
[19:31] that can take actions in the world?
[19:33] So the main way that we do this is
[19:37] through tools. So a tool is something
[19:40] that's situated in the environment um
[19:42] which will uh provide an interface for
[19:44] the model to interact with that
[19:46] environment. And you could think of this
[19:49] as being like um an API for example like
[19:52] if we want the model to be able to uh uh
[19:54] find out what the weather is so that it
[19:56] could respond to a user asking about
[19:59] that maybe we have um an API for like
[20:02] you know weather.gov which is wrapped in
[20:04] an interface that allows the model to
[20:06] call it. So there's a bunch of different
[20:08] ways to represent this interface. Graham
[20:10] will be covering them in more detail I
[20:12] think in the next lecture but here's one
[20:14] example. This is the open AI um tool
[20:18] specification where um for a given tool
[20:20] aka function that the model can call.
[20:23] You'll have a name for that tool um a
[20:25] natural language description of what it
[20:27] does. So for example, read file might be
[20:30] a tool that a coding agent uses to uh
[20:33] look at files in the repo that it's
[20:36] acting in. We'll also need to tell the
[20:38] model what it can pass to this function.
[20:40] So we'll have a description of um the
[20:43] parameters that it takes like maybe this
[20:45] function just takes a path which is a
[20:48] string you know for the file to open. So
[20:50] we have to uh so we have the name and
[20:51] description we have some structured
[20:54] representation of the interface to the
[20:58] function which here is JSON and um this
[21:01] also needs to get fed into the model in
[21:04] some way. So we'll have um this you know
[21:07] underlying specification of the tool and
[21:10] then the model will view it by applying
[21:12] this template which turns it into a
[21:14] sequence of text which will then be
[21:17] tokenized and read by the OM which uh
[21:19] might look like this and the model will
[21:23] have to be um uh sort of either trained
[21:26] or with few examples um know how to use
[21:28] these tools.
[21:30] So this is how the model becomes aware
[21:32] of the tools that it can use to interact
[21:35] with the environment. But the model will
[21:38] also be needing to use those tools to
[21:41] interact and it does this through tool
[21:44] calls. So for example generating text
[21:47] like this like tool call and then you
[21:49] specify the name of the function that
[21:51] you want to call and the arguments as
[21:53] well if you're using sort of a JSONbased
[21:56] representation. Can anybody make a
[21:57] suggestion for another way that you
[22:15] >> Yeah, you could just write code
[22:18] directly. for example, bash scripts or
[22:20] if you represented this as a Python
[22:22] function, the model could just, you
[22:24] know, call the function using Python
[22:25] syntax. And we'll see in a couple
[22:27] lectures that that's actually a very
[22:29] effective and often more effective way
[22:31] than generating JSON. Um, but there's
[22:34] some trade-offs, too. So, when the model
[22:36] calls the tool, it'll get back results
[22:38] from executing that tool in the
[22:40] environment. So for example, if we're
[22:43] reading um this test file, maybe that
[22:46] test file has this code for an add
[22:48] function in it and um the environment
[22:52] will return um you know the results of
[22:54] that tool in this content field and then
[22:56] that'll be rendered to the model using a
[22:58] template um which the model will then
[23:00] read in as tokens and get to continue
[23:02] producing output. Any questions about
[23:09] Cool. So now that we kind of have like
[23:12] the basic tool interface, we're able to
[23:14] um have the language model use these
[23:17] tools to act in the environment. So the
[23:19] way it does this is just by reading in
[23:21] these token sequences that represent
[23:24] what tools are available um uh that
[23:27] represent uh the results of tools and
[23:29] then um generating token sequences
[23:31] naming the tools which then invokes
[23:33] them.
[23:35] And so this uh we have this distinction
[23:37] between the language model itself which
[23:40] is just you know interacting with tokens
[23:42] um later on we'll talk about multimodal
[23:44] language models which maybe also take in
[23:47] images or other modalities. Um so the
[23:49] language models just tokens in and
[23:51] tokens out maybe multimodal tokens but
[23:53] then there's this harness which is
[23:56] responsible for actually um coordinating
[23:58] um these tool calls um using the
[24:03] language model as an engine for it.
[24:05] And so the agentive loop basically and
[24:08] tool former was a really impactful paper
[24:10] that showed that you can train models to
[24:12] be able to use tool calls and then
[24:15] condition on the results of those to um
[24:18] make future text more likely and showed
[24:19] an early way that you could train these
[24:21] models to use tools um that generalized
[24:25] prior LLM training procedures.
[24:27] So once you have this basic setup that
[24:29] you then can implement an agent by
[24:32] running um a loop um and one of the
[24:35] influential papers here was called react
[24:37] um from 2023 um which stands for
[24:39] reasoning and acting because the model's
[24:40] producing chains of thought and then
[24:43] taking actions afterwards and the way it
[24:47] works is you'll have some uh context um
[24:49] which you know includes maybe a
[24:51] definition of the general task of
[24:54] solving pull requests on GitHub or solve
[24:55] issues on GitHub. We'll see some
[24:57] examples of this in a bit. Then you have
[25:00] a task which is maybe an initial query
[25:03] from the user. Um you'll also have a
[25:05] list of all the tools that are available
[25:06] for the agent to call which will be
[25:08] represented using one of those formats
[25:10] that we showed. And you'll also have a
[25:13] history of the past um observations and
[25:16] actions that the agent um has produced
[25:19] and observed as it's been interacting.
[25:22] And in each uh at each time step um so
[25:24] for a given particular state the agent's
[25:26] in it's going to condition on all of
[25:29] that produce a reasoning chain um you
[25:32] know chain of thought um with a scratch
[25:34] pad about what it should do and then
[25:36] produce um one or more tool calls that
[25:38] will be used to interact with the
[25:40] environment or with the user. So for
[25:44] example reading the file. So that tool
[25:45] call will get executed in the
[25:47] environment. We get the results. We add
[25:50] those results to the history and um the
[25:53] environment is also getting updated as a
[25:55] result of our tool call and then we
[25:56] repeat the process again. So the model's
[25:59] conditioning on this updated history and
[26:01] you know the observations that it gets
[26:03] from this time step and then issues a
[26:05] new tool call and it repeats over and
[26:08] over. We could also have tool calls that
[26:10] end the task that for example send a
[26:13] message to the user um or otherwise
[26:16] signal completion. Um and uh so this is
[26:18] a way that we can you know signal that
[26:19] we are finished. And in the planning
[26:20] lecture we'll talk a little bit about
[26:23] like how might a model determine that
[26:25] it's done.
[26:27] So I won't get into the details of this
[26:30] too much. Um you'll get into it when you
[26:32] do assignment one which asks you to
[26:37] implement a um react style loop to uh
[26:39] implement a small coding agent and use
[26:42] it to solve problems in a repo um a a
[26:44] chess engine repo actually. So there's
[26:47] some fun demos that go with it too. Um
[26:48] so we won't get too much into the
[26:50] details of this and the code that you
[26:52] will write will look different than this
[26:54] but you know at a high level this is a
[26:57] very simple implementation. This is an
[27:00] excerpt from this nice minimal repo
[27:03] called mini sui Asian um which actually
[27:07] gets very high performance um on the
[27:09] bench benchmark which we'll talk about
[27:12] in a few lectures. It's a very standard
[27:15] um benchmark for coding agents. Um but
[27:17] it's a really nice repo that I'd
[27:19] encourage you to take a look at because
[27:22] um it's um effective with recent models,
[27:24] but it's also pretty simple and really
[27:27] kind of distills um you know the the
[27:31] distills the basics down. Um but you'll
[27:33] uh start off by having some messages uh
[27:35] which give the model context about it
[27:38] being an agent and about the task. And
[27:40] then you'll just uh run this loop over
[27:42] and over again that implements what we
[27:44] had on the past slide where the agent
[27:46] will um issue a query to a language
[27:49] model using all of the past u messages
[27:53] which contain the history um and then uh
[27:55] it'll add that message to the history
[28:02] and um execute um the uh execute uh the
[28:04] actions in the environment. And we've
[28:06] left this off, but you can take a look
[28:08] at the code repo if you're interested.
[28:09] Execute the actions, get the
[28:14] observations, and um return them.
[28:16] So, I think it's also instructive to
[28:17] take a look at example agent
[28:20] trajectories. And um one nice thing
[28:23] about the Swebench uh data set or
[28:26] Swebench evaluation task and leaderboard
[28:28] is that they have some example
[28:31] trajectories here. Um so, let's take a
[28:34] look at maybe
[28:38] GPTO OSS.
[28:40] And this can give you a feel for what uh
[28:42] tool calls can look like and what the
[28:45] model is actually seeing um as it's
[28:48] carrying out this task. So let's see if
[28:57] Yeah. So the model gets some uh context
[29:00] in a system message um which says you
[29:02] are a helpful assistant that can
[29:04] interact with a computer shell. So this
[29:07] is like very generic um but then we'll
[29:10] also have a user message which gives
[29:12] some context about a particular task uh
[29:16] solving this particular um poll request.
[29:21] and so the model conditions on all of
[29:24] that and then it needs to um issue a
[29:26] first action and you can see here the
[29:28] chain of thought trace that it
[29:30] generates. So this blue is generated by
[29:32] the model. So you have the chain of
[29:34] thought here and it produces a tool
[29:37] call. This agent is using the um the
[29:40] tool format that you suggested which is
[29:43] just issuing bash commands um by you
[29:45] know writing the uh command that should
[29:47] be run that gets handed off to the
[29:49] environment. The environment executes it
[29:51] and here the result is just an exit code
[29:54] exit code zero showing it succeeded but
[29:56] then we go on to the next turn and the
[29:58] agent uh you know issues a new thought
[30:02] and a new bash command and so on.
[30:04] So hopefully that gives you a sense of
[30:06] you know one possible way of uh
[30:09] instantiating tools and instantiating
[30:11] prompts and you'll experiment with this
[30:19] Cool. So uh now I'll hand over to
[30:36] Thanks a lot. Okay. Hi. Uh
[30:39] I guess uh everyone can hear me. So next
[30:41] I'd like to talk about agent
[30:43] capabilities. And what I mean by this is
[30:47] like what makes a good agent. Uh because
[30:50] as uh Daniel pointed out uh it's not
[30:52] very hard to make an agent. uh
[30:53] especially nowadays that there are
[30:56] libraries that you can call to you know
[30:57] do inference with a language model or
[31:00] something like this. The hard part is
[31:02] making one that actually works. Um so
[31:05] I'd like to think a little bit about uh
[31:07] the capabilities that you need to have
[31:11] in an agent. So a fairly large number of
[31:13] people said they use agents in some way
[31:15] you know every day like openclaw or
[31:17] coding agents. Um what are the things
[31:19] that frustrate you when you use an
[31:21] agent? like what what has gone wrong
[31:23] that was a problem? We saw an example of
[31:24] deleting all your email files. That
[31:27] would probably frustrate you, but um any
[31:29] any other things?
[31:31] >> They're too slow.
[31:34] >> Okay. Yeah, that that's a good one.
[31:38] Uh in the backy
[31:40] wordy and verbose. That's a good one. I
[31:57] >> They might misunderstand what you said
[32:06] >> Do doing what was it?
[32:08] >> Like accessing things they shouldn't be
[32:10] accessing. Yeah. Okay. That that's a
[32:18] random knowledge gaps for very common or
[32:19] normal things. Yeah, that that's a good
[32:27] >> Yeah. Writing a thousand lines of code
[32:29] when two would do. Yes, that that's a
[32:31] good one. That's kind of a different
[32:32] variety of verbose, but it's also Yeah.
[32:38] >> Yeah. Forgetting previous session
[32:43] interactions. So, um, yeah.
[32:45] >> Not knowing how to push back when you
[32:49] say something, uh, unreasonable. Yeah.
[32:52] >> They may lie to you. Yes, that's a bad
[32:59] >> A lot of implicit assumptions. Yeah. So,
[33:02] um, these are all great points. Um, all
[33:05] things that frustrate me, too. So um
[33:07] they're they don't exactly align with
[33:08] what I had on the slide but you know
[33:13] that's a a great uh a great thing. So um
[33:15] a first capability that you need to have
[33:18] uh in agents is accurate tool calling.
[33:20] This is something that actually nobody
[33:22] mentioned uh because a lot of people
[33:25] take it for granted nowadays but this is
[33:27] not something you can take for granted
[33:31] uh if you're starting this class and
[33:33] you're in charge of training the model.
[33:36] Um so uh you know it's kind of bread and
[33:38] butter. If you can't call tools
[33:39] accurately you're going to fail at any
[33:43] task you do. But uh it's something that
[33:45] doesn't come for free. Another thing is
[33:47] coherence over long context. And so
[33:49] somebody said uh it annoys me when they
[33:52] forget things or it annoys me when they
[33:53] forget the previous sessions or
[33:55] something like this. So uh that that's
[33:58] one example of it. Another example of it
[34:01] is uh what the example that Daniel gave
[34:03] where previously the model was told to
[34:05] not do something but then it ended up
[34:07] doing it anyway. So uh that that's
[34:09] another example.
[34:12] Another thing is uh customizability. And
[34:14] so
[34:16] you want the agent to do things your
[34:19] way. Uh everybody has different uh ways
[34:21] of doing things uh different
[34:22] requirements. So our class might have a
[34:24] different requirement than another
[34:26] class. And so you need to make sure that
[34:28] if you're using an agent uh it's going
[34:30] to follow those requirements.
[34:33] Uh complex task management. So breaking
[34:36] down tasks uh being able to handle very
[34:38] long horizon things is a very big uh
[34:40] very big issue.
[34:42] environment understanding and what I
[34:45] mean by this is uh there were like one
[34:47] good example of this is making a
[34:49] thousand line change in a codebase where
[34:53] two lines would do that's an implicit
[34:55] failure of environment understanding to
[34:57] know that you know this is actually a
[34:58] really simple change but it didn't
[35:00] realize that and it goes and does a
[35:02] bunch of other things instead and then a
[35:06] final thing is safety and a lot of
[35:08] people separate safety and capabilities
[35:10] they say I'm a safety researcher or I'm
[35:12] a capabilities researcher. But from my
[35:15] point of view, capability safety is a
[35:17] capability. It's something you need to
[35:19] bake into the model. And if it's not
[35:22] baked into the model, you won't feel
[35:24] like you won't feel comfortable using
[35:26] the model because it might go off and do
[35:27] something that you don't uh want it to
[35:30] do. And so from my point of view, it's a
[35:32] a failure of the model or the agent more
[35:35] broadly.
[35:37] And so there's two ways to build these
[35:38] capabilities. And this is something
[35:40] that's really really important when
[35:43] you're working on agents. Uh the first
[35:47] one is uh training in LLM. The second
[35:50] one is engineering the harness uh so
[35:52] that you put structure around the LLM to
[35:57] get it to uh you know solve uh like
[35:58] solve the problems you want in the way
[36:02] that you want to. So
[36:06] question um which one do you think is
[36:11] more important or effective uh here? So
[36:12] does anyone have an a strong opinion
[36:15] that LLM training is the way to to get
[36:24] Okay, actually surprisingly large small
[36:26] number of people. What about um train uh
[36:27] engineering the harness around the
[36:29] agents?
[36:32] Okay, that that's a pretty large number
[36:34] of people. I saw Daniel raised his hand
[36:36] twice, so he's not allowed to do that,
[36:38] but [laughter]
[36:41] um he's the instructor. So, of course,
[36:44] both of these uh are important. Um my my
[36:48] personal opinion um or well, first I'll
[36:49] I'll you know talk a little bit about
[36:51] what they entail. So, the first one is
[36:53] changing the model's behavior through
[36:55] pre-training uh supervised fine-tuning
[36:58] or reinforcement learning. Um and then
[37:00] you can teach uh reusable patterns for
[37:03] reasoning, tool use and recovery.
[37:05] The important thing is the capabilities
[37:07] become part of the learn model or the
[37:09] learned uh policy. And so in harness
[37:11] engineering, you change the system
[37:12] around the model. You give it prompts,
[37:15] tools, memories and control flow provide
[37:17] context, validation, retries and safety
[37:20] boundaries. And the capabilities emerge
[37:22] not just from the model, but they emerge
[37:24] from the combination of the harness and
[37:26] the model.
[37:30] So my my answer to this is
[37:33] um they're they're maybe both important
[37:36] but typically what happens is you
[37:38] identify a problem and you solve it here
[37:40] first.
[37:42] Then
[37:45] the people who are training the models
[37:48] uh catch up and realize that this is a
[37:49] big problem. It's a big enough problem
[37:51] that it warrants them training the model
[37:52] in a particular way to solve the
[37:55] problem. it gets solved and you don't
[37:57] need to solve it in the harness side
[38:00] anymore. So that this is a typical flow.
[38:02] Um
[38:06] so from my point of view this is kind of
[38:08] very often the more fundamental solution
[38:09] on the left side but it takes a lot of
[38:12] time and so you eventually you need to
[38:13] start out by solving it on the right
[38:15] side because you don't have the time uh
[38:17] when you're improving your models. So I
[38:19] I personally favor LLM training as a
[38:21] fundamental solution to problems if
[38:22] you're in a situation where you're able
[38:37] >> So, this is a great question. So, what
[38:40] are the capabilities that will survive
[38:44] LLM training? Um, one I can definitively
[38:48] say is long context uh in like
[38:51] maintaining all of your your memories uh
[38:54] in context because
[38:57] there that is not a
[39:00] that's not a model
[39:02] accuracy problem only. It's also a model
[39:04] efficiency problem. So you need to be
[39:07] able to model very long sequences. And
[39:09] sure you might be able to come up with a
[39:11] model that doesn't have like n squ
[39:15] complexity like the transformer does but
[39:19] you know that's uh you know that's kind
[39:20] of a bigger a bigger discussion assuming
[39:21] we're staying in our our current
[39:32] most of the other stuff I have on here
[39:35] uh
[39:36] most of the other stuff I have on here.
[39:39] Accurate tool calling, uh, coherence
[39:42] within your context window, complex task
[39:46] management, environment understanding,
[39:48] mostly from a capabilities perspective
[39:50] can be and maybe even safety mostly from
[39:53] a capabilities perspective could be
[39:54] theoretically solved through the model,
[39:56] but they're not solved yet. Um, and so
[39:59] we still need uh we still need harness
[40:01] uh engineering. Customizability is a
[40:03] very interesting one because you could
[40:06] train the model on the fly. Um, but
[40:08] there are also cases where you kind of
[40:10] want to give it like a script or you
[40:12] want to give it separate instructions
[40:13] based on the situation that you're in
[40:15] and they're like maybe training it would
[40:17] not be the best solution. But we can
[40:18] talk a lot more about you know all of
[40:32] >> Yeah. So um a follow-up question on when
[40:35] inference uh latency is very important
[40:37] is engineering the harness to fit the
[40:41] problem a good solution. So uh
[40:42] what what I want to point out is all of
[40:44] these capabilities can be handled either
[40:46] through training or through the harness.
[40:50] Um and so I I wouldn't say like one is
[40:51] necessarily always better than the
[40:53] other. They're both uh both solutions.
[40:55] The interesting thing about like
[40:59] inference time uh efficiency is you need
[41:01] often need to use a weaker model or you
[41:03] need to use less compute and because
[41:04] that's the case you often need to put
[41:06] more guard rails around it because
[41:07] you're going to have less su uh success
[41:10] or you need to do like adaptation to the
[41:12] particular task you're interested in. So
[41:14] um the the smaller the model you're
[41:16] using the more careful you need to be
[41:18] because the very big models can often
[41:19] generalize better. Um they're not
[41:22] perfect but they can generalize better.
[41:23] Cool.
[41:26] Uh any others?
[41:30] Okay. So um
[41:35] moving on to uh onto this. So um one of
[41:38] the big goals of this class is to get
[41:41] people to be able get all of you to be
[41:44] able to train a model uh for agentic
[41:49] tasks. And this is uh a big point in
[41:52] that not that many people can do this
[41:54] well. And so we'd like the people in
[41:55] this room to be not that many people,
[41:57] right? We we'd like you to be good at at
[42:00] something that that's hard to do, but uh
[42:03] hard to do, right? But, you know, um
[42:05] like it's a good thing to know how to do
[42:07] if you do know how to do it. Um we're
[42:09] not going to be handling pre-training uh
[42:11] because pre-training uh you know, it's
[42:13] on the scale of the entire internet and
[42:16] that's uh unfortunately not something
[42:19] our our modal credits uh will support.
[42:21] uh but we will be uh thinking about
[42:23] mid-training and supervised fine-tuning
[42:26] and reinforcement learning. And uh the
[42:28] points here are mid-training and
[42:29] supervised fine-tuning is where you
[42:32] already have example demonstrations of
[42:33] how an agent did a task and you're
[42:36] training on those example demonstrations
[42:38] uh usually by optimizing maximum
[42:40] likelihood. Hopefully everybody in this
[42:41] class has done that before because it's
[42:45] a prerequisite for the class. So um uh
[42:47] we'll only be covering that briefly and
[42:49] be focusing more on how you create the
[42:51] data for doing this in indogentic
[42:53] setting. Um and then we're going to
[42:56] focus more uh on reinforcement learning
[42:59] because reinforcement learning for uh
[43:02] like agents is is pretty tricky. So how
[43:03] many people have done reinforcement
[43:06] learning with language models before? I
[43:08] guess maybe not that many people. Yeah.
[43:10] Okay. How many have done it for
[43:11] reasoning
[43:14] reasoning tasks? How many have done it
[43:17] for agents?
[43:19] Okay, maybe about half and half and it's
[43:22] only like maybe 10 10% 10% and 80% have
[43:24] not done it. So yeah, we're going to try
[43:25] to put a lot of effort into making sure
[43:27] that everybody is able to do this by the
[43:30] end of the class.
[43:32] Cool. Um so looking at all the
[43:34] capabilities one by one. Um, accurate
[43:36] tool calling is uh an important
[43:39] capability to have. Uh, we do it through
[43:41] harness engineering and LLM training.
[43:43] Uh, some of the things we're going to
[43:45] talk about in class are grammar
[43:47] constraint decoding, uh, which allows
[43:49] you to make sure that your tool calls
[43:50] are wellformed and match the
[43:53] specification that you have. Um, for LLM
[43:56] training, this is
[44:00] first done through SFT um or through uh
[44:01] through mid training or or whatever you
[44:03] want to call it. Um and this is done by
[44:05] training on tool calling uh tool calling
[44:08] data tool calling traces.
[44:15] for coherence uh over long context uh
[44:17] this again can be done through harness
[44:21] engineering or uh or LLM training. For
[44:22] harness engineering, we do this through
[44:25] context compression or compaction which
[44:28] are kind of synonyms um where you take
[44:30] all of the context and you summarize it
[44:32] down uh for the agent to continue
[44:35] working. It also can be done through
[44:37] dynamic memory lookup uh where you have
[44:39] memory over all the context that you
[44:40] want to be handling but you don't pull
[44:44] it all in immediately uh you pull it uh
[44:47] in you know on demand. Um and it can
[44:48] also be done through sub aent
[44:50] delegation. So you delegate some parts
[44:53] of a very long task to an agent. It
[44:54] keeps that context in memory, but then
[44:56] it drops it out of memory when it's done
[44:58] performing that.
[45:01] Um for LLM training, uh you can do that
[45:02] through long context training. We're not
[45:04] going to handle it a lot, but we'll talk
[45:08] about it maybe a little bit. Um
[45:10] then for customizability, this is
[45:11] actually one of the best use cases for
[45:14] harness engineering uh right now, I
[45:16] think. And there's a bunch of methods
[45:17] that you can do this. Uh one is through
[45:19] agent memory. So making sure that the
[45:22] agent continues to learn uh as you
[45:25] interact with it more um through skills
[45:28] uh which are kind of
[45:32] prompts and sometimes scripts about uh
[45:33] the sort of thing that you want to do
[45:36] that you pull in at each uh time peri
[45:37] time time point when you want to use
[45:41] those things. Um also possibly custom
[45:44] tools for a particular task.
[45:48] um for LM training uh this is a nent
[45:49] area. I don't think there's a lot of
[45:52] people who are doing this in uh in a lot
[45:54] of detail. Uh but there are methods
[45:56] where you can learn from user feedback.
[45:59] And so like if a user is is using a tool
[46:01] and they give a thumbs up or a thumbs
[46:02] down, you can learn specifically from
[46:06] them to adapt to them.
[46:08] Complex task management. Uh ways you can
[46:10] do this are through harness uh
[46:12] engineering. So you can provide planning
[46:15] or decomposition tools. You can have a
[46:18] plan mode uh for the model where uh it
[46:22] uh it gets to plan. I this is a little
[46:24] uh thing that I I learned but there was
[46:26] a popular coding harness I think it was
[46:29] uh codeex no sorry maybe it was clog
[46:31] code where they had a plan mode and uh
[46:33] the only thing when people pressed the
[46:35] plan mode button was that it added an
[46:37] extra thing to the prompt that said
[46:40] please plan do not do anything. Um,
[46:40] [laughter]
[46:42] but everybody wanted a plan mode. They
[46:44] wanted a button. So, they made sure that
[46:45] it was done entirely through prompts.
[46:48] But there's also more uh more complex
[46:51] ways uh to do this as well. Um, again,
[46:53] you can do this through sub aent
[46:54] delegation by like breaking down the
[46:57] task and uh delegating it to other
[46:59] agents. And a very good way to do this
[47:02] in training is to train on complex uh
[47:05] long horizon tasks.
[47:07] So for environment understanding, what I
[47:11] mean by this is whatever data format or
[47:12] environment that your agent is uh
[47:14] interacting with, it needs to be able to
[47:17] understand it. And just to give one very
[47:19] good example of this in computer use
[47:22] agents, um you need to be able to
[47:26] understand web pages and or uh you know
[47:29] guey interfaces or something like this.
[47:31] This is not something you get for free.
[47:33] In fact, like agents are actually pretty
[47:35] bad at it right now. Uh even the
[47:38] strongest agents are maybe not, but like
[47:40] um many of the open source models don't
[47:44] even support multimodal uh data and uh
[47:47] like the ones that do are not perfect at
[47:48] understanding it. They make lots of
[47:49] mistakes, many more than when they're
[47:53] understanding text. So this is a failure
[47:55] of uh understanding the environment
[47:56] because they need to understand the
[47:58] multi- modal data in their environment.
[47:59] But now let's put them in a different
[48:01] environment where they need to trade
[48:05] stocks or something like that. Um,
[48:06] they're not very good at understanding
[48:07] time series. They make a lot of mistakes
[48:09] on time series. Or you put them in an
[48:11] environment where they need to
[48:16] understand a picture of a, you know, a
[48:18] petri dish with lots of bacteria in it
[48:19] or something like that. They fail to do
[48:22] that as well. So you kind of need to be
[48:23] able to understand whatever environment
[48:26] you want the agents to uh, you know,
[48:29] interact with. So there's ways you can
[48:31] do this through hardness engineering by
[48:33] like giving skills that correspond to
[48:35] domain knowledge but you can also train
[48:38] on data with the expected observation
[48:40] shape or train in domain specific
[48:41] environments.
[48:46] So right now actually like
[48:47] there's kind of this thing uh that
[48:49] people say which is like oh the models
[48:51] are going to get better uh and then we
[48:53] won't need to worry about that anymore.
[48:57] Um the thing is models don't get better.
[49:00] Uh people make models better. And so one
[49:01] of the things we'd like to teach in the
[49:03] class is like what's actually going on
[49:04] under the hood when suddenly Claude goes
[49:08] from uh 4.7 to 4.8 and it can suddenly
[49:12] like compose music better. Um, and the
[49:14] there's a few things uh that go into
[49:17] this, but one of the really big ones is
[49:19] uh they make an environment to train the
[49:22] model on uh a like compose music
[49:24] environment and suddenly you know they
[49:27] they train on it for you know they add
[49:28] it to the training mix and then the
[49:30] model gets better at composing music or
[49:32] something. So a lot of the uh a lot of
[49:34] the work here is creating domain
[49:35] specific environments that models can
[49:38] work in.
[49:40] Uh then the final thing is safety. And
[49:43] uh we're going to talk about it for uh
[49:46] like a bit because if you don't have a
[49:47] safe model, you're not going to be able
[49:49] to use it in real consequential
[49:51] settings. Um and there's a lot of things
[49:53] with respect to harness engineering that
[49:54] you can do here. You can give it a
[49:57] sandbox. Um you can limit access to cred
[49:59] credentials. You can also monitor the
[50:03] agent as it works. Um and you can also
[50:05] do safetyaware reinforcement learning.
[50:08] Um I I think probably a fair number of
[50:09] people heard about this, but who heard
[50:13] about the OpenAI incident where uh it
[50:17] hacked into hugging face? Okay. Well, so
[50:19] I think most people heard about it, but
[50:22] recently there was a um there was an
[50:25] example where uh the newest open AAI
[50:27] model was in an agentic harness and it
[50:29] was working on a cyber security
[50:33] benchmark and so its instruction was
[50:36] hack into this system and so it was
[50:38] going to hack into a system and that was
[50:41] its task and it wasn't able to hack into
[50:43] the system. So instead it basically
[50:45] hacked into the hugging face website and
[50:47] uh and got the answers from the hugging
[50:50] face website and and did it there. And
[50:52] so there were a bunch of failures that h
[50:56] that happened here. Um the first failure
[50:58] was a failure in sandboxing because they
[51:00] didn't properly contain the agent when
[51:02] it was doing this benchmark.
[51:04] um they
[51:07] they did have limited access to
[51:09] credentials and so it worked around that
[51:11] problem uh by by hacking into something
[51:14] it didn't have credentials for. Um and
[51:15] they also didn't have sufficient
[51:16] monitoring so they weren't able to tell
[51:19] that this happened. Uh they didn't have
[51:20] sufficient safety guardrails on this
[51:22] model because this model was being
[51:27] trained to test uh you know like whether
[51:28] it could hack into systems. So
[51:29] presumably the models that they
[51:31] eventually released to the public did
[51:33] have better guardrails of this model.
[51:36] But like um these are all ways that you
[51:37] can handle safety and we'll be talking
[51:40] about this sort of thing as well.
[51:43] So the final thing um and any questions
[51:45] about the capabilities part. We're going
[51:47] to go into a lot more detail of course.
[51:49] So
[51:52] okay, sounds good. Um so another thing
[51:55] that I we really want to reinforce here
[51:58] is agents are systems. uh they're not
[52:01] just models and they are far more
[52:04] complex than most of the things you've
[52:07] dealt with in any
[52:09] machine learning class that you've taken
[52:11] any you know class here that you've
[52:13] taken before. So you're going to have to
[52:16] be able to handle a bunch of different
[52:19] things. The first thing is a harness.
[52:22] Um, which is a
[52:26] moderate to complex piece of software.
[52:28] Um, and it has a lot of moving parts
[52:29] like you need to deal with the context,
[52:32] you need to deal with the the tools, uh,
[52:35] the guardrails, manage workflows, uh,
[52:38] stuff like that. Um, you need to have a
[52:40] sandbox. So, you need to make sure the
[52:42] agent is working within a contained
[52:45] environment. And, um, there are
[52:47] different ways you can do that. uh it
[52:49] needs to work with a model and you need
[52:51] to do inference. But if you've done
[52:53] inference with language models before,
[52:55] you might have dealt with contexts of
[53:00] like 16 tokens or 32 uh 16k tokens or
[53:05] 32k tokens. Here you need like 256 uh at
[53:07] least they have kind of like a
[53:09] state-of-the-art uh coding agent for
[53:11] instance. And so um the inference
[53:12] problems are harder. You need to deal
[53:14] with caching your inference other things
[53:16] like that. and you need monitoring and
[53:18] training.
[53:21] So um from the point of view of this
[53:22] what we're going to teach in the class
[53:25] is harness engineering. So um how to
[53:28] manage state tools memory control flow
[53:30] um how to validate actions, handle
[53:32] errors, enforce permission and safety
[53:36] boundaries. Um and we're in for each of
[53:37] these systems, we're also going to try
[53:40] to give examples of software uh that you
[53:43] can look at. Um, for harnesses, there's
[53:45] kind of two big varieties of harness
[53:49] that you use for coding agents. Um, some
[53:52] popular ones right now are cloud code,
[53:54] codecs, open hands, open code, and pi.
[53:57] Uh, probably you know you're you have
[54:00] used or have heard of uh at least one of
[54:03] these. Um, I develop open hands so I
[54:05] know it very well. Uh, and so I'll be
[54:07] talking about uh talking about this. I'd
[54:08] also like to give a little bit of my
[54:10] experience and some of the lessons we
[54:13] learned uh in in developing it.
[54:16] Separately from this um there are
[54:18] orchestrators. I I wrote lang chain but
[54:20] maybe I should have written lang graph
[54:22] instead in crew AI and kind of the they
[54:24] have a very different philosophy between
[54:27] these. Um the the coding agents are are
[54:30] generally simpler uh in terms of how
[54:33] different intera uh agents interact with
[54:34] each other but they're more complex in
[54:36] the action space that you give to the
[54:38] agent. So the agent can write code, it
[54:40] can interact with a website, it can do
[54:43] other stuff like this. Um orchestrators
[54:45] are less complex with respect to the
[54:47] individual agent that they have. So the
[54:50] agent might just be able to answer
[54:52] customer service requests or um look
[54:54] something up in a database, but it
[54:55] couldn't write an arbitrary Python
[54:57] program. But on the other hand, you get
[54:59] like these
[55:02] declarative workflows of what the agent
[55:04] workflow is able to do. And so that's
[55:05] like a a different way of building
[55:07] things. It's more guardrail but less
[55:09] expressive. And they both have their
[55:12] place uh in different settings.
[55:14] For sandboxing uh to prevent your agents
[55:17] from uh
[55:19] sharing your API keys without your
[55:22] permission or uh hacking into other
[55:24] websites. Um we need to isolate code and
[55:27] tool execution and limit the compute
[55:29] network and file system access that
[55:32] agents have uh access to. Um another big
[55:33] thing is for evaluation and training.
[55:35] It's a very good way to create
[55:38] reproducible environments. Uh so like
[55:41] for SWEBench for instance each problem
[55:44] has a uh each problem has a sandbox and
[55:45] you start in the sandbox and that's the
[55:47] state of the environment before the
[55:50] agent starts working and so you can run
[55:53] these uh locally. Um some of the uh
[55:55] technologies that we use for this are
[55:58] Docker and Appainer. Um or you can run
[56:03] them on the cloud and uh two of our uh
[56:04] kind of compute partners for this class
[56:08] Modal and sale are uh like cloud uh in
[56:10] uh providers and actually prime
[56:13] intellect for that matter.
[56:15] So the next thing is uh language model
[56:17] inference. And so I I think you know
[56:20] given your previous experience in an in
[56:22] an NLP or like large language model
[56:25] class presumably most people have uh
[56:29] encountered this before but basically um
[56:32] they uh are required to serve model
[56:34] gener generations
[56:37] um batch requests. So if you have like
[56:38] multiple agents hitting your language
[56:40] model at once, it's more efficient but
[56:41] also you need to batch the requests
[56:43] together.
[56:46] An extremely extremely important part of
[56:49] agents is caching previous requests
[56:51] because agents take more and more
[56:53] actions and so the more and more actions
[56:55] they take the more uh kind of context
[56:57] they build up and you need to make sure
[57:00] that you reuse that to do it um uh
[57:02] properly and you know other systems
[57:04] considerations.
[57:06] Uh some example software that we're
[57:07] going to talk about here is uh things
[57:09] like VLM and SGLANG. These are the two
[57:11] most popular ones. And then there is
[57:13] also tons and tons of inference
[57:15] providers. Um if people have not seen
[57:18] open router before, open router is kind
[57:19] of a a general thing that gathers
[57:21] together all the inference providers.
[57:25] And for any model, uh you'll see like 20
[57:26] or 30 different providers serving the
[57:27] models. So there's lots and lots of
[57:29] them. uh one of our compute sponsors
[57:34] fireworks is an example of that and sale
[57:37] um training systems. So here what they
[57:40] do is uh basically they need to update
[57:42] the models weights and so they uh
[57:45] prepare data, collect rollouts um uh
[57:47] they coordinate a whole bunch of workers
[57:49] who are working together uh to to train
[57:52] the models and they can uh checkpoint
[57:55] evaluate and reproduce runs. Um some
[57:57] example pieces of software here are Sky
[58:01] RL and Miles. Um and so uh the these can
[58:04] be used for for training.
[58:06] And finally um observability and
[58:08] monitoring. Uh so this is uh to
[58:10] understand how your agents are working.
[58:13] So these capture the traces or
[58:14] trajectories of the agent, what the
[58:17] agent did um and they gather metrics
[58:19] around them uh such as like how much
[58:21] time it takes, how much cost it was uh
[58:23] track the quality, the cost and the
[58:25] failures. Um and they allow you to
[58:27] compare trajectories and evaluations.
[58:31] And so um uh I'm I'm pretty familiar
[58:33] with one called Laminer because I use it
[58:36] a lot. MLFlow is another example. Um I I
[58:37] just realized that Daniel showed one
[58:40] called transluce uh which is not on my
[58:42] slide here but that's another another
[58:45] popular one.
[58:48] So um by the end of the class what I
[58:49] hope everybody in the class would be
[58:52] able to do is uh implement an agent from
[58:55] scratch uh on top of an open source LLM.
[58:57] So uh this is implement a harness
[58:59] yourself uh design evaluations for
[59:02] multi-step tasks. And so basically uh
[59:04] we'll give you a task that you need to
[59:05] evaluate and you need to create an
[59:09] evaluation for it. This is super super
[59:11] important even if you're not interested
[59:13] in evaluation but you're also interested
[59:15] in training because one of the best ways
[59:17] to do training is to create an
[59:20] evaluation and scale it uh so that you
[59:22] can do reinforcement learning based
[59:25] training. So um very important skill to
[59:28] have uh train agents to improve their
[59:30] capabilities. So we actually run the RL
[59:32] loop, handle all the systems problems
[59:35] and be able to to solve this um reason
[59:36] about safety and reliability trade-offs.
[59:39] So we'll we'll be talking about safety
[59:41] and uh finally we will have a project
[59:43] which I'll I'll talk about on the next
[59:45] slide.
[59:47] So um these are the assignments. Um the
[59:49] first assignments are basically going to
[59:51] be implementation assignments. So you'll
[59:54] be given uh something to do and be asked
[59:56] to do it. And uh the first one is create
[01:00:00] a harness. Um the second one is
[01:00:03] evaluation as I measured as I I read
[01:00:06] measure as I mentioned. Um and then uh
[01:00:09] training uh where we train with RL. And
[01:00:11] so these are approximately the first
[01:00:14] half of the course. Um and then the
[01:00:16] second half of the course will be to do
[01:00:19] a project uh using these skills uh to
[01:00:21] you know do something kind of
[01:00:24] interesting or novel uh in whatever area
[01:00:26] you choose. And the project will be
[01:00:29] group based. So we're going to be uh
[01:00:31] asking you to form groups of two or
[01:00:34] three and uh and create a project. And
[01:00:36] the general schedule is uh we're going
[01:00:39] to talk about agent capabilities first.
[01:00:41] Um we're then going to jump into some
[01:00:42] specific domains like coding and guey
[01:00:48] agents. Um do uh training uh and uh
[01:00:52] including SFT and RL. Um we're going to
[01:00:53] be talking about uh frameworks and
[01:00:57] safety. And then uh we're going to be
[01:00:58] talking about interaction and then we
[01:01:00] have some project hours where everybody
[01:01:03] uh discusses their projects. And then uh
[01:01:05] on the end of the class we're going to
[01:01:07] try to get uh some domain experts from
[01:01:09] each of the various domains to give a
[01:01:12] guest lecture um which maybe combines a
[01:01:13] little bit of overview but also their
[01:01:16] research. Uh and so uh hopefully you'll
[01:01:18] be able to learn from uh some pretty
[01:01:21] exciting people. And I uh Daniel and I
[01:01:23] tried to brainstorm the best people in
[01:01:25] the uh in the world to talk about their
[01:01:26] things and I don't know if anybody said
[01:01:29] no. Um
[01:01:32] so I think everybody said yes. So uh we
[01:01:34] we got our first choice for every every
[01:01:37] topic. So I'm pretty excited about that.
[01:01:39] Um
[01:01:42] so uh before we begin uh we have some
[01:01:46] prerequisites and this is a heavy course
[01:01:48] in terms of implementation in machine
[01:01:50] learning. Uh we want uh we want
[01:01:52] everybody to be able to train an agent
[01:01:55] with RL by the end of it. And so our
[01:01:58] prerequisite is also um we require prior
[01:02:00] serious experience training a language
[01:02:04] model. Um the LTI courses on uh language
[01:02:06] models, language model systems, NLP
[01:02:08] would all qualify for this prerequisite.
[01:02:09] So if you took one of those, that's
[01:02:11] okay. Um some deep learning courses
[01:02:14] might qualify for it. Uh if you're not
[01:02:17] sure, um feel free to ask us. Um but we
[01:02:18] are going to require this and we're
[01:02:20] going to have everybody have to submit a
[01:02:23] form for it. So uh please uh please do
[01:02:27] do that. Um if there's like 30 people
[01:02:28] who want to know whether their course
[01:02:31] qualifies, please don't ask me that
[01:02:33] specific question after the class here
[01:02:35] because it'd be better to do it through
[01:02:37] email, but um uh other questions we'll
[01:02:39] be happy to answer after the class. Um
[01:02:42] we'll share a Google form on Patza and
[01:02:43] please submit the form so we can
[01:02:47] finalize enrollment. Um and uh yeah, I I
[01:02:51] already um uh I already covered it. If
[01:02:52] you haven't taken a course, if you've
[01:02:54] worked in industry and you've trained a
[01:02:57] model in industry, uh it should be a
[01:03:00] real one like at least 4 to 7B uh size,
[01:03:03] not uh not 100 million parameters. Um
[01:03:12] Um and so uh this is the grading policy.
[01:03:14] Um so assignments one to three will be
[01:03:18] 40% total uh completed individually. Um
[01:03:21] we're going to have lecture highlights
[01:03:24] and so uh basically the idea here is
[01:03:27] that we want people to uh
[01:03:30] come to the lecture and
[01:03:34] uh give a highlight about you know
[01:03:36] something you learned in the lecture.
[01:03:40] The idea around this is not to be, you
[01:03:42] know, not to make people do like undo
[01:03:44] work or something like this, but if you
[01:03:47] watch through the entire lecture, you
[01:03:48] hopefully you came up with something
[01:03:50] that's interesting. If you said if you
[01:03:52] could say nothing was interesting, I
[01:03:54] knew all of this already. I learned it
[01:03:56] here uh in this previous class that's
[01:03:58] already in the prerequisite list. That's
[01:04:00] also useful information for us. So share
[01:04:02] it with us. But hopefully we'll say at
[01:04:03] least one interesting thing in every
[01:04:06] lecture. So uh you can uh you can follow
[01:04:10] up with that. Um the research project uh
[01:04:13] is uh 50% of the total um and this will
[01:04:15] be in teams of two to three uh because
[01:04:18] it's uh half of the class assignments.
[01:04:20] Um the proposal is 5%, the check-in is
[01:04:23] 5%, presentation is 10% and final report
[01:04:26] is 30%. And if you've taken an LTI uh
[01:04:28] project based class before, grading will
[01:04:30] be similar to the LTI project based
[01:04:33] class uh requirements. Um if you have
[01:04:37] not then uh we'll we'll be sharing uh
[01:04:44] Um so here's the question uh you've all
[01:04:47] been asking for. This is an AI agent
[01:04:52] class. Um and we discussed this very
[01:04:54] um very thoroughly about what we wanted
[01:04:58] to do here. Um,
[01:05:00] I'd like to preface this by saying I use
[01:05:01] agents all the time for nearly
[01:05:05] everything I do. Um, but at the same
[01:05:07] time, it's kind of dangerous to use
[01:05:09] agents for everything because you lose
[01:05:12] like sight of uh of what you want to uh
[01:05:15] like of what you're learning. You miss
[01:05:16] some of the details and other things
[01:05:19] like this because the goal of this class
[01:05:22] is learning. Um but we also want
[01:05:23] everybody to be familiar with the
[01:05:28] standard practice. Um we uh we want you
[01:05:32] to keep this in mind and uh AI tools
[01:05:36] will be permitted um for basically
[01:05:38] everything in the course unless we say
[01:05:39] otherwise and we probably won't be
[01:05:44] saying otherwise very often. Um so uh
[01:05:46] lecture highlights must be written by
[01:05:50] you not generated by AI. Um and so these
[01:05:52] do not need to be long. Uh they can be
[01:05:54] short, they can be a few sentences, but
[01:05:57] please uh write them yourself. And uh
[01:05:59] you are responsible for every submitted
[01:06:02] claim, citation, result in line of code.
[01:06:06] And uh we will create quizzes uh for the
[01:06:09] assignments so that uh you will you may
[01:06:12] need to explain uh parts of your code.
[01:06:15] And uh how will we do this? Uh we also
[01:06:22] We we are considering having agents read
[01:06:24] uh read your code and come up with quiz
[01:06:28] questions tailored to your code. Um so
[01:06:31] uh we're we're serious about this. Uh
[01:06:33] and that means that the thousand lines
[01:06:36] of slop that your agent generated will
[01:06:38] be a bad idea for you to submit. Um so
[01:06:40] it's better to submit something concise
[01:06:42] that you really understand well uh than
[01:06:44] uh submitting you know more uh
[01:06:46] basically.
[01:06:49] Um, so yeah, uh, we're almost done. Uh,
[01:06:52] deadlines, uh, submissions in Slack. So,
[01:06:54] all the assignments, uh, include two
[01:06:57] 24-hour Slack days. Um, they cannot be
[01:06:59] transferred or shared. After the Slack
[01:07:01] days are used, the penalty is 5% of the
[01:07:03] assignment score per additional day or
[01:07:06] part day. So, what this means is the
[01:07:09] deadline is the deadline. And, uh, but
[01:07:11] we're being nice and if you miss the
[01:07:13] deadline, we'll give you some time to
[01:07:16] make up for it. uh if you miss the
[01:07:20] deadline by more than two days um then
[01:07:23] uh we're not going to take most excuses.
[01:07:25] If you you were in the hospital or
[01:07:27] something like that, we uh might ask you
[01:07:29] to get appropriate acknowledgement of
[01:07:31] that, but that would be an example uh
[01:07:33] reason why. Uh but other than that,
[01:07:35] please try to meet the deadline because
[01:07:36] we're not going to make many exceptions
[01:07:40] to this. Um cool, that's all. Uh we're
[01:07:44] at 441. Um so which means we have nine
[01:07:46] minutes for questions if people have
[01:07:49] questions. Um otherwise uh looking
[01:07:50] forward to having everybody in the
