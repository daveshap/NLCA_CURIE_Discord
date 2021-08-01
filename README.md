# Raven Discord - Barebones

This is an ultra-lightweight barebones version of NLCA using only CURIE (GPT-3) and SQLITE. Consider this the training-wheels version. Since this will use CURIE the prompts should be portable to other technologies like GPT-J.

## Architecture

![Discord Architecture](https://github.com/daveshap/RavenDiscord3/blob/main/Discord%20Architecture%203.png)

## Shared DB Service

### Fields (Schema)

- type
- content
- time (created time)
- last_access
- access_count
- uuid
- parent
- vector?
- summary?