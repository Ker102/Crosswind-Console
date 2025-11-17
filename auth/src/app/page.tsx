import Link from 'next/link'
import { getServerSession } from 'next-auth'

import { authOptions } from '@/lib/authOptions'

export default async function Home() {
  const session = await getServerSession(authOptions)

  return (
    <main style={{ padding: '3rem', fontFamily: 'var(--font-sans)', lineHeight: 1.5 }}>
      <h1>Auth service</h1>
      <p>
        This Next.js instance exposes NextAuth (Google OAuth) and the `/api/progress` endpoint for
        persisting dashboard state.
      </p>
      <section style={{ marginTop: '2rem' }}>
        <h2>Status</h2>
        {session?.user ? (
          <div>
            <p>Signed in as {session.user.email ?? session.user.name}</p>
            <p>User ID: {session.user.id}</p>
            <Link href="/api/auth/signout">Sign out</Link>
          </div>
        ) : (
          <div>
            <p>You are not signed in.</p>
            <Link href="/api/auth/signin">Sign in with Google</Link>
          </div>
        )}
      </section>
    </main>
  )
}
