'use client'

import { useState, useEffect } from 'react'
import { useAuth } from '@/lib/auth'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Skeleton } from '@/components/ui/skeleton'
import { motion } from 'framer-motion'
import AppShell from '@/components/AppShell'
import {
  Users, FileText, CheckSquare, Clock, GraduationCap,
  ChevronRight, UserCheck, AlertCircle, School, BarChart3, ClipboardList
} from 'lucide-react'
import { useRouter } from 'next/navigation'

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1'

const statusMap = {
  pending: 'warning',
  approved: 'success',
  rejected: 'destructive',
  enrolled: 'info',
}

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

export default function CoordinatorDashboard() {
  return <AppShell><CoordinatorDashboard_ /></AppShell>
}
function CoordinatorDashboard_() {
  const { user, loading } = useAuth()
  const router = useRouter()
  const [stats, setStats] = useState(null)
  const [students, setStudents] = useState([])
  const [loadingData, setLoading] = useState(true)

  useEffect(() => {
    if (loading || user?.role !== 'department_coordinator') return
    async function load() {
      try {
        const token = localStorage.getItem('token')
        const headers = { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' }
        const [statsRes, studentsRes] = await Promise.all([
          fetch(`${API_BASE}/coordinator/dashboard`, { headers }),
          fetch(`${API_BASE}/coordinator/students`, { headers }),
        ])
        if (statsRes.ok) setStats(await statsRes.json())
        if (studentsRes.ok) setStudents(await studentsRes.json())
      } catch (e) {
        console.error('Failed to load coordinator data', e)
      } finally {
        setLoading(false)
      }
    }
    load()
  }, [user, loading])

  if (loadingData) {
    return (
      <div className="space-y-6">
        <Skeleton className="h-8 w-56" />
        <div className="grid gap-4 md:grid-cols-4">
          {[...Array(4)].map((_, i) => <Skeleton key={i} className="h-28 rounded-xl" />)}
        </div>
      </div>
    )
  }

  const totalApplicants = stats?.total_applicants || 0
  const pendingReview = stats?.pending_review || 0
  const approved = stats?.approved || 0
  const enrolled = stats?.enrolled || 0

  return (
    <div className="space-y-8">
      {/* Header */}
      <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} className="flex items-center justify-between">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <ClipboardList className="w-5 h-5 text-emerald-500" />
            <h1 className="text-2xl sm:text-3xl font-bold text-foreground">Department Dashboard</h1>
          </div>
          <p className="text-muted-foreground">Review applicants and manage department admissions</p>
        </div>
        <Badge variant="outline" className="gap-1.5">
          <School className="w-3.5 h-3.5" />
          {stats?.department_name || 'Your Department'}
        </Badge>
      </motion.div>

      {/* Stats */}
      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <StatCard label="Total Applicants" value={totalApplicants} icon={Users} color="indigo" delay={0.1} />
        <StatCard label="Pending Review" value={pendingReview} icon={Clock} color={pendingReview > 0 ? 'amber' : 'slate'} delay={0.15} />
        <StatCard label="Approved" value={approved} icon={UserCheck} color="emerald" delay={0.2} />
        <StatCard label="Enrolled" value={enrolled} icon={GraduationCap} color="blue" delay={0.25} />
      </div>

      {/* Pending Review Alert */}
      {pendingReview > 0 && (
        <motion.div initial={{ opacity: 0, x: -12 }} animate={{ opacity: 1, x: 0 }} className="flex items-center gap-3 p-4 rounded-xl bg-amber-50 dark:bg-amber-500/5 border border-amber-200/50 dark:border-amber-800/50">
          <AlertCircle className="w-5 h-5 text-amber-600 dark:text-amber-400 flex-shrink-0" />
          <div className="flex-1">
            <p className="text-sm font-medium text-amber-800 dark:text-amber-300">{pendingReview} applicant(s) awaiting review</p>
            <p className="text-xs text-amber-600 dark:text-amber-400">Review and approve/reject pending applications</p>
          </div>
          <Button size="sm" onClick={() => router.push('/coordinator/applications')}>
            Review Now <ChevronRight className="w-3.5 h-3.5 ml-1" />
          </Button>
        </motion.div>
      )}

      {/* Recent Applicants */}
      <motion.div initial={{ opacity: 0, y: 16 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.2 }}>
        <div className="flex items-center justify-between mb-3">
          <div>
            <h2 className="section-title">Recent Applicants</h2>
            <p className="section-desc">Latest students applying to your department</p>
          </div>
          <Button variant="outline" size="sm" onClick={() => router.push('/coordinator/applications')}>
            View All <ChevronRight className="w-3.5 h-3.5 ml-1" />
          </Button>
        </div>
        <Card>
          <CardContent className="p-0">
            {students.length === 0 ? (
              <div className="py-12 text-center">
                <Users className="w-12 h-12 text-muted-foreground/30 mx-auto mb-3" />
                <p className="text-sm text-muted-foreground">No applicants for your department yet</p>
              </div>
            ) : (
              <div className="overflow-x-auto">
                <table className="w-full text-sm">
                  <thead>
                    <tr className="border-b border-border bg-muted/50">
                      <th className="text-left py-3 px-4 font-medium text-muted-foreground">Applicant</th>
                      <th className="text-left py-3 px-4 font-medium text-muted-foreground hidden sm:table-cell">Email</th>
                      <th className="text-left py-3 px-4 font-medium text-muted-foreground">Status</th>
                      <th className="text-left py-3 px-4 font-medium text-muted-foreground hidden md:table-cell">Stage</th>
                      <th className="text-right py-3 px-4 font-medium text-muted-foreground">Action</th>
                    </tr>
                  </thead>
                  <tbody>
                    {students.slice(0, 5).map((s) => (
                      <tr key={s.id} className="border-b border-border hover:bg-accent/30 transition-colors">
                        <td className="py-3 px-4">
                          <div className="flex items-center gap-2.5">
                            <div className="h-8 w-8 rounded-full bg-gradient-to-br from-emerald-400 to-teal-500 flex items-center justify-center text-white font-semibold text-xs">
                              {(s.full_name || s.name || '?')[0]}
                            </div>
                            <span className="text-foreground font-medium">{s.full_name || s.name}</span>
                          </div>
                        </td>
                        <td className="py-3 px-4 text-muted-foreground hidden sm:table-cell">{s.email}</td>
                        <td className="py-3 px-4"><Badge variant={statusMap[s.status] || 'secondary'}>{s.status}</Badge></td>
                        <td className="py-3 px-4 text-muted-foreground capitalize hidden md:table-cell">{s.stage || '-'}</td>
                        <td className="py-3 px-4 text-right">
                          <Button variant="ghost" size="sm" onClick={() => router.push(`/coordinator/applications?id=${s.id}`)}>Review</Button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </CardContent>
        </Card>
      </motion.div>

      {/* Department Stats + Quick Actions */}
      <div className="grid gap-6 lg:grid-cols-2">
        <motion.div initial={{ opacity: 0, y: 16 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.3 }}>
          <Card>
            <CardHeader>
              <CardTitle>Department Statistics</CardTitle>
              <CardDescription>Quick overview of department performance</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {[
                  { label: 'Enrollment Rate', value: totalApplicants > 0 ? `${Math.round((enrolled / totalApplicants) * 100)}%` : '\u2014' },
                  { label: 'Average Processing Time', value: stats?.avg_processing_time || '\u2014' },
                  { label: 'Documents Pending', value: stats?.documents_pending || 0 },
                  { label: 'Interviews Scheduled', value: stats?.interviews_scheduled || 0 },
                ].map((item) => (
                  <div key={item.label} className="flex items-center justify-between py-2 border-b border-border last:border-0">
                    <span className="text-sm text-muted-foreground">{item.label}</span>
                    <span className="text-sm font-semibold text-foreground">{item.value}</span>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </motion.div>

        <motion.div initial={{ opacity: 0, y: 16 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.35 }}>
          <Card>
            <CardHeader>
              <CardTitle>Quick Actions</CardTitle>
              <CardDescription>Tools and reports</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-2">
                <button onClick={() => router.push('/coordinator/reports')}
                  className="w-full flex items-center gap-3 p-3 rounded-lg border border-border hover:bg-accent/50 transition-colors text-left">
                  <BarChart3 className="w-4 h-4 text-emerald-500" />
                  <div className="flex-1">
                    <p className="text-sm font-medium text-foreground">Generate Reports</p>
                    <p className="text-xs text-muted-foreground">Admission and department reports</p>
                  </div>
                  <ChevronRight className="w-4 h-4 text-muted-foreground" />
                </button>
                <button onClick={() => router.push('/coordinator/students')}
                  className="w-full flex items-center gap-3 p-3 rounded-lg border border-border hover:bg-accent/50 transition-colors text-left">
                  <Users className="w-4 h-4 text-emerald-500" />
                  <div className="flex-1">
                    <p className="text-sm font-medium text-foreground">Browse All Students</p>
                    <p className="text-xs text-muted-foreground">View all department students</p>
                  </div>
                  <ChevronRight className="w-4 h-4 text-muted-foreground" />
                </button>
              </div>
            </CardContent>
          </Card>
        </motion.div>
      </div>
    </div>
  )
}
