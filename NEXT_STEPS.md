# Next steps
1. Review the pull request before merging.
2. After merge, wait for GitHub Pages deployment and open the published URL.
3. Deploy the FastAPI backend separately on a trusted HTTPS host.
4. Set a long random backend bearer token in the backend environment and enter the same token in the app Settings.
5. Configure CORS to allow only your GitHub Pages origin.
6. Integrate an AI provider on the server only; never expose its key in browser code.
7. Test on Android Chrome: install PWA, microphone permission, Hindi/Marathi voice availability, offline shell, notes and history.

The included API chat route is a placeholder response, not model inference. SQLite is local to the backend host and may require a persistent disk.
