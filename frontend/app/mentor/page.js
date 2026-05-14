'use client'

import { useState, useEffect } from 'react'
import { useAuth } from '@/lib/auth'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Skeleton } from '@/components/ui/skeleton'
import { motion } from 'framer-motion'
import AppShell from '@/components/AppShell'
import {
  Users, GraduationCap, Clock, BookOpen, Calendar,
  Star, TrendingUp, AlertCircle, ChevronRight, FileText, MessageCircle
} from 'lucide-react'
import { useRouter } from 'next/navigation'

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1'

const colors = {
  indigo: 'bg-indigo-100 dark:bg-indigo-500/10 text-indigo-600 dark:text-indigo-400',
  emerald: 'bg-emerald-100 dark:bg-emerald-500/10 text-emerald-600 dark:text-emerald-400',
  amber: 'bg-amber-100 dark:bg-amber-500/10 text-amber-600 dark:text-amber-400',
  rose: 'bg-rose-100 dark:bg-rose-500/10 text-rose-600 dark:text-rose-400',
  blue: 'bg-blue-100 dark:bg-blue-500/10 text-blue-600 dark:text-blue-400',
  slate: 'bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400',
}

function StatCard({ label, value, icon: Icon, color = 'indigo', delay = 0 }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 16 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4, delay }}
      className="stats-card"
    >
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm font-medium text-muted-foreground">{label}</p>
          <p className="text-2xl font-bold text-foreground mt-0.5">{value}</p>
        </div>
        {Icon && (
          <div className={`h-11 w-11 rounded-xl flex items-center justify-center flex-shrink-0 ${colors[color]}`}>
            <Icon className="w-5 h-5" />
          </div>
        )}
      </div>
    </motion.div>
  )
}

export default function MentorDashboard() {
  return <AppShell><MentorDashboard_ /></AppShell>
}
function MentorDashboard_() {
  const { user, loading } = useAuth()
  const router = useRouter()
  const [stats, setStats] = useState(null)
  const [students, setStudents] = useState([])
  const [loadingData, setLoading] = useState(true)

  useEffect(() => {
    if (loading || user?.role !== 'mentor') return
    async function load() {
      try {
        const token = localStorage.getItem('token')
        const headers = { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' }
        const [statsRes, studentsRes] = await Promise.all([
          fetch(`${API_BASE}/mentor/stats`, { headers }),
          fetch(`${API_BASE}/mentor/students`, { headers }),
        ])
        if (statsRes.ok) setStats(await statsRes.json())
        if (studentsRes.ok) setStudents(await studentsRes.json())
      } catch (e) {
        console.error('Failed to load mentor data', e)
      } finally {
        setLoading(false)
      }
    }
    load()
  }, [user, loading])

  if (loadingData) {
    return (
      <div className="space-y-6">
        <Skeleton className="h-8 w-48" />
        <div className="grid gap-4 md:grid-cols-3">
          {[...Array(3)].map((_, i) => <Skeleton key={i} className="h-28 rounded-xl" />)}
        </div>
      </div>
    )
  }

  const totalStudents = stats?.total_students || students.length || 0
  const enrolledCount = stats?.enrolled || 0
  const pendingCount = stats?.pending || 0
  const atRiskCount = stats?.at_risk || 0

  return (
    <div className="space-y-8">
      {/* Header */}
      <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} className="flex items-center justify-between">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <Star className="w-5 h-5 text-amber-500" />
            <h1 className="text-2xl sm:text-3xl font-bold text-foreground">Mentor Dashboard</h1>
          </div>
          <p className="text-muted-foreground">Guide and support your assigned students</p>
        </div>
        <Badge variant="premium" className="gap-1.5">
          <Star className="w-3.5 h-3.5 text-amber-500" />
          Faculty Mentor
        </Badge>
      </motion.div>

      {/* Stats */}
      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <StatCard label="Assigned Students" value={totalStudents} icon={Users} color="indigo" delay={0.1} />
        <StatCard label="Enrolled" value={enrolledCount} icon={GraduationCap} color="emerald" delay={0.15} />
        <StatCard label="Pending" value={pendingCount} icon={Clock} color={pendingCount > 0 ? 'amber' : 'slate'} delay={0.2} />
        <StatCard label="Needs Attention" value={atRiskCount} icon={AlertCircle} color={atRiskCount > 0 ? 'rose' : 'slate'} delay={0.25} />
      </div>

      {/* At-risk Alert */}
      {atRiskCount > 0 && (
        <motion.div initial={{ opacity: 0, x: -12 }} animate={{ opacity: 1, x: 0 }}
          className="flex items-center gap-3 p-4 rounded-xl bg-rose-50 dark:bg-rose-500/5 border border-rose-200/50 dark:border-rose-800/50">
          <AlertCircle className="w-5 h-5 text-rose-600 dark:text-rose-400 flex-shrink-0" />
          <div className="flex-1">
            <p className="text-sm font-medium text-rose-800 dark:text-rose-300">{atRiskCount} student(s) need attention</p>
            <p className="text-xs text-rose-600 dark:text-rose-400">Check their progress and schedule a meeting</p>
          </div>
          <Button size="sm" variant="outline" onClick={() => router.push('/mentor/students')}>
            View <ChevronRight className="w-3.5 h-3.5 ml-1" />
          </Button>
        </motion.div>
      )}

      {/* Assigned Students */}
      <motion.div initial={{ opacity: 0, y: 16 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.2 }}>
        <div className="flex items-center justify-between mb-3">
          <div>
            <h2 className="section-title">Assigned Students</h2>
            <p className="section-desc">Students under your mentorship</p>
          </div>
          <Button variant="outline" size="sm" onClick={() => router.push('/mentor/students')}>
            View All <ChevronRight className="w-3.5 h-3.5 ml-1" />
          </Button>
        </div>
        <Card>
          <CardContent className="p-0">
            {students.length === 0 ? (
              <div className="py-12 text-center">
                <Users className="w-12 h-12 text-muted-foreground/30 mx-auto mb-3" />
                <p className="text-sm text-muted-foreground">No students assigned to you yet</p>
              </div>
            ) : (
              <div className="divide-y divide-border">
                {students.slice(0, 5).map((s) => (
                  <div key={s.id} className="flex items-center justify-between p-4 hover:bg-accent/30 transition-colors cursor-pointer"
                    onClick={() => router.push(`/mentor/students?id=${s.id}`)}>
                    <div className="flex items-center gap-3">
                      <div className="h-10 w-10 rounded-full bg-gradient-to-br from-amber-400 to-orange-500 flex items-center justify-center text-white font-semibold">
                        {(s.full_name || s.name || '?')[0]}
                      </div>
                      <div>
                        <p className="text-sm font-medium text-foreground">{s.full_name || s.name}</p>
                        <p className="text-xs text-muted-foreground">{s.email}{s.department ? ` \u00b7 ${s.department}` : ''}</p>
                      </div>
                    </div>
                    <div className="flex items-center gap-2">
                      <Badge variant={s.status === 'enrolled' ? 'success' : s.status === 'pending' ? 'warning' : 'secondary'}>
                        {s.status || 'active'}
                      </Badge>
                      <ChevronRight className="w-4 h-4 text-muted-foreground" />
                    </div>
                  </div>
                ))}
              </div>
            )}
          </CardContent>
        </Card>
      </motion.div>

      {/* Quick Actions */}
      <motion.div initial={{ opacity: 0, y: 16 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.3 }} className="grid gap-6 lg:grid-cols-3">
        <button onClick={() => router.push('/mentor/notes')}
          className="flex items-center gap-3 p-4 bg-card rounded-xl border border-border hover:shadow-elevated transition-all text-left">
          <div className="h-10 w-10 rounded-lg bg-blue-100 dark:bg-blue-500/10 flex items-center justify-center">
            <FileText className="w-5 h-5 text-blue-600 dark:text-blue-400" />
          </div>
          <div className="flex-1">
            <p className="text-sm font-semibold text-foreground">Mentor Notes</p>
            <p className="text-xs text-muted-foreground">Add and review student notes</p>
          </div>
          <ChevronRight className="w-4 h-4 text-muted-foreground" />
        </button>

        <button onClick={() => router.push('/mentor/schedule')}
          className="flex items-center gap-3 p-4 bg-card rounded-xl border border-border hover:shadow-elevated transition-all text-left">
          <div className="h-10 w-10 rounded-lg bg-emerald-100 dark:bg-emerald-500/10 flex items-center justify-center">
            <Calendar className="w-5 h-5 text-emerald-600 dark:text-emerald-400" />
          </div>
          <div className="flex-1">
            <p className="text-sm font-semibold text-foreground">Schedule</p>
            <p className="text-xs text-muted-foreground">Manage mentoring sessions</p>
          </div>
          <ChevronRight className="w-4 h-4 text-muted-foreground" />
        </button>

        <button onClick={() => router.push('/mentor/students')}
          className="flex items-center gap-3 p-4 bg-card rounded-xl border border-border hover:shadow-elevated transition-all text-left">
          <div className="h-10 w-10 rounded-lg bg-amber-100 dark:bg-amber-500/10 flex items-center justify-center">
            <TrendingUp className="w-5 h-5 text-amber-600 dark:text-amber-400" />
          </div>
          <div className="flex-1">
            <p className="text-sm font-semibold text-foreground">Student Progress</p>
            <p className="text-xs text-muted-foreground">Track academic performance</p>
          </div>
          <ChevronRight className="w-4 h-4 text-muted-foreground" />
        </button>
      </motion.div>
    </div>
  )
}
