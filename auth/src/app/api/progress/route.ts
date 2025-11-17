import { NextResponse } from 'next/server'
import { getServerSession } from 'next-auth'

import { authOptions } from '@/lib/authOptions'
import { prisma } from '@/lib/prisma'

const allowedOrigin = process.env.FRONTEND_ORIGIN ?? 'http://localhost:5173'

function withCors(response: NextResponse) {
  response.headers.set('Access-Control-Allow-Origin', allowedOrigin)
  response.headers.set('Access-Control-Allow-Credentials', 'true')
  response.headers.set('Access-Control-Allow-Headers', 'Content-Type, Authorization')
  response.headers.set('Access-Control-Allow-Methods', 'GET,POST,OPTIONS')
  return response
}

export async function OPTIONS() {
  return withCors(new NextResponse(null, { status: 204 }))
}

export async function GET(request: Request) {
  const session = await getServerSession(authOptions)
  if (!session?.user?.id) {
    return withCors(NextResponse.json({ error: 'Unauthorized' }, { status: 401 }))
  }

  const { searchParams } = new URL(request.url)
  const domain = searchParams.get('domain')
  if (!domain) {
    return withCors(NextResponse.json({ error: 'Missing domain parameter' }, { status: 400 }))
  }

  const record = await prisma.progress.findUnique({
    where: {
      userId_domain: {
        userId: session.user.id,
        domain,
      },
    },
  })

  return withCors(
    NextResponse.json(
      {
        domain,
        prompt: record?.prompt,
        payload: record?.payload ? JSON.parse(record.payload) : null,
        updatedAt: record?.updatedAt ?? null,
      },
      { status: 200 }
    )
  )
}

export async function POST(request: Request) {
  const session = await getServerSession(authOptions)
  if (!session?.user?.id) {
    return withCors(NextResponse.json({ error: 'Unauthorized' }, { status: 401 }))
  }

  const body = await request.json()
  const { domain, prompt, payload } = body as {
    domain?: string
    prompt?: string
    payload?: unknown
  }

  if (!domain) {
    return withCors(NextResponse.json({ error: 'Domain is required' }, { status: 400 }))
  }

  const serializedPayload = JSON.stringify(payload ?? {})

  const record = await prisma.progress.upsert({
    where: {
      userId_domain: {
        userId: session.user.id,
        domain,
      },
    },
    update: {
      prompt,
      payload: serializedPayload,
    },
    create: {
      userId: session.user.id,
      domain,
      prompt,
      payload: serializedPayload,
    },
  })

  return withCors(
    NextResponse.json(
      {
        domain: record.domain,
        prompt: record.prompt,
        payload: JSON.parse(record.payload),
        updatedAt: record.updatedAt,
      },
      { status: 200 }
    )
  )
}
