# Auth Service (NextAuth + Prisma)

This Next.js app exposes Google OAuth via NextAuth along with a `/api/progress` endpoint that stores dashboard state for signed-in users. It is meant to run alongside the FastAPI backend + Svelte frontend.

## Prerequisites
- Node.js 18+
- Google Cloud project with OAuth credentials (web client ID/secret)
- Values populated in the repo root `.env` (copied from `.env.example`)

## Environment
The scripts in `package.json` automatically load the root `.env` via `dotenv-cli`. Make sure the following keys are set:

```
GOOGLE_CLIENT_ID=...
GOOGLE_CLIENT_SECRET=...
NEXTAUTH_SECRET=... # `openssl rand -base64 32`
NEXTAUTH_URL=http://localhost:3001
FRONTEND_ORIGIN=http://localhost:5173
DATABASE_URL=file:./prisma/dev.db
```

For Google OAuth: whitelist `http://localhost:3001/api/auth/callback/google` as the redirect URI.

## Database
The Prisma schema lives in `prisma/schema.prisma`. Run once to create/update the SQLite database:

```bash
cd auth
set -a && source ../.env && set +a
npx prisma migrate dev --name init
```

(If the schema engine is finicky on your system, `npx prisma db push` is an alternative.)

## Development

```bash
cd auth
npm run dev -- --port 3001
```

This starts Next.js on port 3001 so it can coexist with Vite (5173) and FastAPI (8000). Visit `http://localhost:3001` to trigger a Google sign-in or hit the helper endpoints:

- `GET /api/session` – session snapshot with CORS headers for the Svelte app
- `GET|POST /api/progress` – persist or hydrate per-domain insights for the signed-in user

## Deployment Notes
- Keep this service behind HTTPS in production so Google OAuth redirects succeed.
- Use a managed database (Neon, Supabase, etc.) by switching `DATABASE_URL` and re-running Prisma migrations.
- Adjust `FRONTEND_ORIGIN` + `NEXTAUTH_URL` to match your deployed hosts for clean CORS + callback behavior.
