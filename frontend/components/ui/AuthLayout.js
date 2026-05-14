'use client'

import { motion } from 'framer-motion'
import { Sparkles, Shield, Zap, ArrowRight } from 'lucide-react'
import { useEffect, useState } from 'react'

const features = [
  { icon: Sparkles, label: 'AI-Powered Admission', desc: 'Smart application processing' },
  { icon: Shield, label: 'End-to-End Encryption', desc: 'Your data stays secure' },
  { icon: Zap, label: 'Real-Time Processing', desc: 'Instant updates & notifications' },
]

const floatingElements = [
  { size: 'w-64 h-64', color: 'bg-indigo-500/10', x: '10%', y: '20%', delay: 0 },
  { size: 'w-48 h-48', color: 'bg-purple-500/10', x: '60%', y: '10%', delay: 2 },
  { size: 'w-72 h-72', color: 'bg-pink-500/8', x: '20%', y: '50%', delay: 4 },
  { size: 'w-40 h-40', color: 'bg-indigo-500/8', x: '70%', y: '60%', delay: 1 },
  { size: 'w-56 h-56', color: 'bg-blue-500/8', x: '50%', y: '70%', delay: 3 },
]

export default function AuthLayout({ children, title, subtitle }) {
  const [mounted, setMounted] = useState(false)
  useEffect(() => { setMounted(true) }, [])

  return (
    <div className="min-h-screen flex bg-gradient-to-br from-slate-50 via-indigo-50/30 to-slate-50 dark:from-slate-950 dark:via-indigo-950/20 dark:to-slate-950">
      {/* Brand Panel - Left */}
      <div className="hidden lg:flex lg:w-[480px] xl:w-[520px] flex-col relative overflow-hidden bg-gradient-to-br from-indigo-950 via-indigo-900 to-purple-950">
        {/* Animated background blobs */}
        {mounted && floatingElements.map((el, i) => (
          <motion.div
            key={i}
            className={`absolute rounded-full ${el.size} ${el.color} blur-3xl`}
            style={{ left: el.x, top: el.y }}
            animate={{
              x: [0, 30, -20, 0],
              y: [0, -20, 30, 0],
              scale: [1, 1.05, 0.95, 1],
            }}
            transition={{ duration: 8 + i, repeat: Infinity, delay: el.delay, ease: 'easeInOut' }}
          />
        ))}

        {/* Grid pattern overlay */}
        <div className="absolute inset-0 opacity-[0.03]" style={{ backgroundImage: 'linear-gradient(rgba(255,255,255,0.1) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.1) 1px, transparent 1px)', backgroundSize: '40px 40px' }} />

        <div className="relative z-10 flex flex-col h-full p-12">
          {/* Logo */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.6 }}
            className="flex items-center gap-3"
          >
            <div className="w-10 h-10 rounded-xl bg-white/10 backdrop-blur-sm border border-white/10 flex items-center justify-center">
              <span className="text-white font-bold text-lg">S</span>
            </div>
            <span className="text-white font-semibold text-lg">Saarthi</span>
          </motion.div>

          {/* Hero message */}
          <div className="flex-1 flex flex-col justify-center max-w-md">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.2 }}
            >
              <h1 className="text-4xl xl:text-5xl font-bold text-white leading-tight">
                {title || 'Your Smart Admission Companion'}
              </h1>
              <p className="text-indigo-200/80 text-base mt-4 leading-relaxed">
                {subtitle || 'AI-powered platform for seamless engineering admission processing, document verification, and student onboarding.'}
              </p>
            </motion.div>

            {/* Feature pills */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.4 }}
              className="space-y-3 mt-10"
            >
              {features.map((f, i) => {
                const Icon = f.icon
                return (
                  <div key={i} className="flex items-center gap-3 group">
                    <div className="w-9 h-9 rounded-lg bg-white/5 border border-white/10 flex items-center justify-center group-hover:bg-white/10 transition-colors">
                      <Icon className="w-4 h-4 text-indigo-300" />
                    </div>
                    <div>
                      <p className="text-sm font-medium text-white">{f.label}</p>
                      <p className="text-xs text-indigo-300/70">{f.desc}</p>
                    </div>
                  </div>
                )
              })}
            </motion.div>
          </div>

          {/* Footer */}
          <motion.p
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.6, delay: 0.8 }}
            className="text-xs text-indigo-300/50"
          >
            &copy; {new Date().getFullYear()} Saarthi. All rights reserved.
          </motion.p>
        </div>
      </div>

      {/* Form Panel - Right */}
      <div className="flex-1 flex items-center justify-center p-4 sm:p-8 relative overflow-hidden">
        {/* Mobile brand header */}
        <div className="absolute top-0 left-0 right-0 lg:hidden">
          <div className="flex items-center gap-2.5 p-4">
            <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-indigo-600 to-purple-600 flex items-center justify-center">
              <span className="text-white font-bold text-sm">S</span>
            </div>
            <span className="text-sm font-semibold text-slate-900 dark:text-white">Saarthi</span>
          </div>
        </div>

        {/* Animated background */}
        <div className="absolute inset-0 overflow-hidden pointer-events-none">
          <div className="absolute -top-40 -right-40 w-80 h-80 bg-indigo-500/5 rounded-full blur-3xl" />
          <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-purple-500/5 rounded-full blur-3xl" />
        </div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="w-full max-w-md relative z-10"
        >
          {children}
        </motion.div>
      </div>
    </div>
  )
}
