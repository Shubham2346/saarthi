'use client'

import { motion } from 'framer-motion'
import { GraduationCap, Shield, ClipboardList, Users, Terminal } from 'lucide-react'
import { cn } from '@/lib/utils'

const roles = [
  { id: 'student', label: 'Student', icon: GraduationCap, description: 'Apply for admission', color: 'from-indigo-500 to-purple-600' },
  { id: 'admin', label: 'Admin', icon: Shield, description: 'Manage operations', color: 'from-blue-500 to-cyan-600' },
  { id: 'department_coordinator', label: 'Coordinator', icon: ClipboardList, description: 'Department oversight', color: 'from-emerald-500 to-teal-600' },
  { id: 'mentor', label: 'Mentor', icon: Users, description: 'Guide students', color: 'from-amber-500 to-orange-600' },
  { id: 'system_admin', label: 'System Admin', icon: Terminal, description: 'Platform control', color: 'from-rose-500 to-pink-600' },
]

const container = {
  hidden: {},
  show: {
    transition: { staggerChildren: 0.05 },
  },
}

const item = {
  hidden: { opacity: 0, y: 12 },
  show: { opacity: 1, y: 0 },
}

export default function RoleSelector({ selected, onChange, compact }) {
  return (
    <motion.div
      variants={container}
      initial="hidden"
      animate="show"
      className={cn('grid gap-2', compact ? 'grid-cols-5' : 'grid-cols-1 sm:grid-cols-2')}
    >
      {roles.map((role) => {
        const Icon = role.icon
        const isSelected = selected === role.id
        return (
          <motion.button
            key={role.id}
            variants={item}
            type="button"
            onClick={() => onChange(role.id)}
            className={cn(
              'relative flex items-center gap-3 p-3 rounded-xl border text-left transition-all duration-200',
              isSelected
                ? 'border-indigo-500/50 bg-indigo-50 dark:bg-indigo-500/10 shadow-sm shadow-indigo-500/10'
                : 'border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900/50 hover:border-slate-300 dark:hover:border-slate-600 hover:shadow-soft'
            )}
          >
            <div className={cn(
              'w-10 h-10 rounded-xl flex items-center justify-center flex-shrink-0 bg-gradient-to-br text-white',
              isSelected ? role.color : 'from-slate-200 to-slate-300 dark:from-slate-700 dark:to-slate-600'
            )}>
              <Icon className="w-4 h-4" />
            </div>
            <div className="min-w-0">
              <p className={cn('text-sm font-medium', isSelected ? 'text-indigo-600 dark:text-indigo-400' : 'text-slate-700 dark:text-slate-300')}>
                {role.label}
              </p>
              {!compact && (
                <p className="text-xs text-slate-500 dark:text-slate-400 truncate">{role.description}</p>
              )}
            </div>
            {isSelected && (
              <div className="absolute inset-0 rounded-xl ring-1 ring-inset ring-indigo-500/30 pointer-events-none" />
            )}
          </motion.button>
        )
      })}
    </motion.div>
  )
}
