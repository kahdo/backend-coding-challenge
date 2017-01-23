# UnbabelChallengeMultilingualHackerNews [ubcmhn]
##Solution Analysis.

##### Main goals and design guidelines.

- KISS
- Dual-headed, fully detached approach. 
    - 2 working components + Database as the glue. 
    - Threaded/Distributed Component: Keeping the DB updated with new (and translated) content.
    - Web-facing Component: Reading up and rendering content from DB's current state.
        - Gracefully ignore entries being translated or worked on
        - Our content is going to be static, maybe even cache it locally as we update the headlines.
- Minimal grit/intercomm between those two components. Leverage the DB to keep things as atomic as
possible so that the web-facing component does not need to take care of tasks statuses and whatnot.
    - "Status" attribute on the main Document schema to keep both components from shooting each other
    on the foot :-)

