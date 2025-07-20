# LinkedIn Post Generator & Publisher Agent

This example demonstrates a complete LinkedIn content pipeline using the Agent Development Kit (ADK) that not only generates and refines LinkedIn posts but can also automatically publish them to your LinkedIn profile.

## Overview

The LinkedIn Post Generator uses a sequential pipeline with a loop component and LinkedIn API integration to:
1. Generate an initial LinkedIn post
2. Iteratively refine the post until quality requirements are met
3. **Automatically post to your LinkedIn profile** (new feature!)

This demonstrates several key patterns:
1. **Sequential Pipeline**: A multi-step workflow with distinct stages
2. **Iterative Refinement**: Using a loop to repeatedly refine content
3. **Automatic Quality Checking**: Validating content against specific criteria
4. **Feedback-Driven Refinement**: Improving content based on specific feedback
5. **Loop Exit Tool**: Using a tool to terminate the loop when quality requirements are met
6. **🆕 LinkedIn API Integration**: Direct posting to LinkedIn via API
7. **🆕 Real-world Publishing**: Bridge from content generation to actual social media presence

## Architecture

The system is composed of the following components:

### Root Sequential Agent
`LinkedInPostGenerationPipeline` - A SequentialAgent that orchestrates the overall process:
1. First runs the initial post generator
2. Then executes the refinement loop
3. **🆕 Finally publishes to LinkedIn when user confirms**

### Initial Post Generator
`InitialPostGenerator` - An LlmAgent that creates the first draft of the LinkedIn post with no prior context.

### Refinement Loop
`PostRefinementLoop` - A LoopAgent that executes a two-stage refinement process:
1. First runs the reviewer to evaluate the post and possibly exit the loop
2. Then runs the refiner to improve the post if the loop continues

### Sub-Agents Inside the Refinement Loop
1. **Post Reviewer** (`PostReviewer`) - Reviews posts for quality and provides feedback or exits the loop if requirements are met
2. **Post Refiner** (`PostRefiner`) - Refines the post based on feedback to improve quality

### 🆕 LinkedIn Publishing Tools
1. **Post to LinkedIn** - Publishes content directly to your LinkedIn profile
2. **Preview Post** - Shows how the post will appear before publishing
3. **Validate LinkedIn Auth** - Checks if LinkedIn credentials are properly configured

### Quality Control Tools
1. **Character Counter** - Validates post length against requirements (used by the Reviewer)
2. **Exit Loop** - Terminates the loop when all quality criteria are satisfied (used by the Reviewer)

## 🆕 LinkedIn API Integration

### Setup Requirements

1. **LinkedIn Developer Account**: Create an app at [LinkedIn Developer Portal](https://developer.linkedin.com/)
2. **OAuth Configuration**: Set redirect URL to `http://localhost:8080`
3. **Permissions**: Add `w_member_social` scope for posting
4. **Authentication**: Get access token and person ID through OAuth flow

### Environment Configuration

Create a `.env` file with:

```bash
# Google API Key (Required)
GOOGLE_API_KEY=your_google_api_key_here

# LinkedIn API Credentials (Required for posting)
LINKEDIN_ACCESS_TOKEN=your_linkedin_access_token
LINKEDIN_PERSON_ID=your_linkedin_person_id
LINKEDIN_CLIENT_ID=your_linkedin_client_id
LINKEDIN_CLIENT_SECRET=your_linkedin_client_secret
```

### Getting LinkedIn Credentials

Run the authentication helper to get your tokens:

```bash
python linkedin_auth_helper.py
```

This will:
1. Open LinkedIn OAuth in your browser
2. Guide you through the approval process
3. Extract your access token and person ID
4. Provide the credentials for your `.env` file

## Loop Control with Exit Tool

A key design pattern in this example is the use of an `exit_loop` tool to control when the loop terminates. The Post Reviewer has two responsibilities:

1. **Quality Evaluation**: Checks if the post meets all requirements
2. **Loop Control**: Calls the exit_loop tool when the post passes all quality checks

When the exit_loop tool is called:
1. It sets `tool_context.actions.escalate = True`
2. This signals to the LoopAgent that it should stop iterating

## Usage

### Method 1: Web Interface (Recommended)

```bash
cd 12-loop-agent
adk web
```

Then in the web interface, enter a prompt like:
- "Generate a LinkedIn post about AI trends in 2025"
- "Create a post about my experience with Google ADK"
- "Write a professional update about our product launch"

### Method 2: Command Line

```bash
cd 12-loop-agent
python main.py
```

Then interact directly with the agent.

## 🆕 Complete Workflow

The system will:
1. **Generate** an initial LinkedIn post based on your prompt
2. **Review** the post for quality and compliance with LinkedIn best practices
3. **Refine** the post iteratively until it meets all requirements
4. **Preview** the final post showing how it will appear on LinkedIn
5. **Ask for confirmation** before posting
6. **Publish** to your LinkedIn profile if you approve
7. **Provide confirmation** with post URL and engagement tracking

## Example Input & Output

### Input:
```
Generate a LinkedIn post about what I've learned from building AI agents with Google's ADK framework.
```

### Generated Post:
```
🤖 Just completed an incredible journey building AI agents with Google's Agent Development Kit (ADK)! 

Key learnings:
✅ Multi-agent orchestration is game-changing
✅ Tool integration makes agents incredibly powerful  
✅ Loop patterns enable iterative refinement
✅ Real-world deployment is surprisingly straightforward

The future of AI isn't just about better models - it's about intelligent orchestration of specialized agents working together.

What's your experience with multi-agent systems? 

#AI #AgentDevelopmentKit #Google #MachineLearning #Innovation

Ready to post to LinkedIn? (y/n):
```

### Publishing Result:
```
✅ Successfully posted to LinkedIn! 
📊 Post ID: 12345
🔗 View at: https://linkedin.com/posts/yourprofile_12345
```

## Loop Termination

The loop terminates in one of two ways:
1. **Quality Achieved**: When the post meets all requirements (reviewer calls the exit_loop tool)
2. **Max Iterations**: After reaching the maximum number of iterations (10)

## 🆕 Publishing Options

You can choose to:
- **Generate only**: Create and refine content without posting
- **Preview first**: See exactly how the post will look
- **Post publicly**: Share with all LinkedIn connections
- **Post to connections**: Share with your network only

## Security & Privacy

- **OAuth 2.0**: Secure authentication with LinkedIn
- **Token Management**: Access tokens stored locally in `.env`
- **User Confirmation**: Always asks before posting
- **Preview Mode**: See content before it goes live
- **Revokable Access**: Can revoke app permissions anytime

## Troubleshooting

### Common Issues:

1. **LinkedIn Authentication Failed**
   - Check your access token is valid
   - Ensure OAuth redirect URL is correct
   - Verify `w_member_social` permission is granted

2. **Post Rejected by LinkedIn**
   - Content may violate LinkedIn policies
   - Check character limits (3000 max)
   - Ensure proper formatting

3. **API Rate Limits**
   - LinkedIn has posting limits (varies by account type)
   - Wait before retrying
   - Consider batching posts

### Getting Help:

1. Check LinkedIn Developer documentation
2. Verify your app permissions in LinkedIn Developer Portal
3. Test with simple content first
4. Review ADK documentation for agent patterns

---

**Ready to automate your LinkedIn presence?** 🚀

This agent bridges the gap between AI content generation and real-world social media engagement, enabling you to maintain an active, high-quality LinkedIn presence with minimal manual effort.
