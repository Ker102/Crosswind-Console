import { NextResponse } from 'next/server'
import { getServerSession } from 'next-auth'

import { authOptions } from '@/lib/authOptions'

const allowedOrigin = process.env.FRONTEND_ORIGIN ?? 'http://localhost:5173'

function withCors(response: NextResponse) {
  response.headers.set('Access-Control-Allow-Origin', allowedOrigin)
  response.headers.set('Access-Control-Allow-Credentials', 'true')
  response.headers.set('Access-Control-Allow-Headers', 'Content-Type, Authorization')
  response.headers.set('Access-Control-Allow-Methods', 'GET,OPTIONS')
  return response
}

export async function OPTIONS() {
  return withCors(new NextResponse(null, { status: 204 }))
}

export async function GET() {
  const session = await getServerSession(authOptions)
  return withCors(
    NextResponse.json(
      {
        authenticated: Boolean(session),
        session,
      },
      { status: 200 }
    )
  )
}
