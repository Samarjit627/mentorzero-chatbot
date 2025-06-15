# MentorZero Frontend (React + Tailwind)

## Getting Started

1. **Install dependencies:**

   ```bash
   cd frontend
   npm install
   ```

2. **Start the development server:**

   ```bash
   npm run dev
   ```
   The app will run at [http://localhost:3000](http://localhost:3000)

3. **Backend API:**
   - Make sure the FastAPI backend is running at `http://localhost:8000`.
   - The React app proxies `/api` calls to the backend.

---

## Project Structure

- `App.tsx` — Main app logic and state.
- `components/` — Modular UI components (Sidebar, ChatView, ChatInput, etc).
- `index.tsx` — Entry point.
- `index.css` — TailwindCSS imports.
- `vite.config.ts` — Vite config with proxy for API.

---

## Build for Production

```bash
npm run build
```

---

## Customization
- Edit `tailwind.config.js` for theming.
- Update components in `components/` for new features.
