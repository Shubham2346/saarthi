'use client'

import { useState, useEffect } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Input } from '@/components/ui/input'
import { Button } from '@/components/ui/button'
import { Search, MessageCircle } from 'lucide-react'

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1'

export default function MentorStudents() {
  const [students, setStudents] = useState([])
  const [search, setSearch] = useState('')

  useEffect(() => {
    async function load() {
      try {
        const token = localStorage.getItem('token')
        const res = await fetch(`${API_BASE}/mentor/students`, { headers: { Authorization: `Bearer ${token}` } })
        if (res.ok) setStudents(await res.json())
      } catch (e) { console.error(e) }
    }
    load()
  }, [])

  const filtered = students.filter(s =>
    (s.full_name || '').toLowerCase().includes(search.toLowerCase())
  )

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-slate-900 dark:text-white">My Students</h1>
        <p className="text-sm text-slate-500 dark:text-slate-400">View and manage your assigned students</p>
      </div>

      <div className="relative max-w-sm">
        <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
        <Input placeholder="Search students..." value={search} onChange={e => setSearch(e.target.value)} className="pl-9" />
      </div>

      <div className="grid gap-4 md:grid-cols-2">
        {filtered.map((s) => (
          <Card key={s.id}>
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <div className="h-10 w-10 rounded-full bg-indigo-100 dark:bg-indigo-900/30 flex items-center justify-center text-indigo-600 dark:text-indigo-400 font-semibold">
                    {(s.full_name || s.name || '?')[0]}
                  </div>
                  <div>
                    <p className="font-medium text-slate-900 dark:text-white">{s.full_name || s.name}</p>
                    <p className="text-xs text-slate-500">{s.email}</p>
                  </div>
                </div>
                <Badge variant={s.status === 'enrolled' ? 'success' : 'warning'}>{s.status || 'active'}</Badge>
              </div>
              <div className="mt-4 flex items-center justify-between text-sm">
                <span className="text-slate-500">{s.department || 'No department'}</span>
                <Button variant="ghost" size="sm">
                  <MessageCircle className="w-4 h-4 mr-1" /> Message
                </Button>
              </div>
            </CardContent>
          </Card>
        ))}
        {filtered.length === 0 && (
          <div className="col-span-2 text-center py-12 text-slate-500">No students assigned yet</div>
        )}
      </div>
    </div>
  )
}
