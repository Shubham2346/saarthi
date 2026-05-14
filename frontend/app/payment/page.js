'use client'

import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import AppShell from '@/components/AppShell'
import {
  CreditCard, Download, CheckCircle2
} from 'lucide-react'

export default function PaymentPage() {
  return (
    <AppShell>
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-slate-900 dark:text-white">Fee Payment</h1>
        <p className="text-sm text-slate-500 dark:text-slate-400">View and pay your admission fees</p>
      </div>

      <div className="grid gap-6 md:grid-cols-3">
        <div className="md:col-span-2 space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Fee Structure</CardTitle>
              <CardDescription>Breakdown of your admission fees</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {[
                  { label: 'Tuition Fee (Merit Quota)', amount: '₹85,000' },
                  { label: 'Development Fee', amount: '₹12,000' },
                  { label: 'Laboratory Fee', amount: '₹5,000' },
                  { label: 'Library Fee', amount: '₹3,000' },
                  { label: 'Exam Fee', amount: '₹4,000' },
                  { label: 'Student Welfare Fund', amount: '₹2,000' },
                  { label: 'Caution Deposit (Refundable)', amount: '₹10,000' },
                ].map((item) => (
                  <div key={item.label} className="flex items-center justify-between py-2 border-b border-slate-100 dark:border-slate-800 last:border-0">
                    <span className="text-sm text-slate-700 dark:text-slate-300">{item.label}</span>
                    <span className="text-sm font-semibold text-slate-900 dark:text-white">{item.amount}</span>
                  </div>
                ))}
                <div className="flex items-center justify-between pt-3 border-t-2 border-slate-200 dark:border-slate-700">
                  <span className="text-base font-bold text-slate-900 dark:text-white">Total</span>
                  <span className="text-lg font-bold text-indigo-600 dark:text-indigo-400">₹1,21,000</span>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Payment Options</CardTitle>
              <CardDescription>Choose your preferred payment method</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {[
                  { method: 'UPI', desc: 'Google Pay, PhonePe, Paytm', icon: '📱' },
                  { method: 'Net Banking', desc: 'All major banks supported', icon: '🏦' },
                  { method: 'Debit/Credit Card', desc: 'Visa, Mastercard, RuPay', icon: '💳' },
                  { method: 'Demand Draft', desc: 'In favor of the college', icon: '📄' },
                ].map((p) => (
                  <div key={p.method} className="flex items-center justify-between p-4 rounded-lg bg-slate-50 dark:bg-slate-800/50 hover:bg-slate-100 dark:hover:bg-slate-800 cursor-pointer transition-colors">
                    <div className="flex items-center gap-3">
                      <span className="text-xl">{p.icon}</span>
                      <div>
                        <p className="text-sm font-medium text-slate-900 dark:text-white">{p.method}</p>
                        <p className="text-xs text-slate-500">{p.desc}</p>
                      </div>
                    </div>
                    <Button size="sm">Pay Now</Button>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>

        <div className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Payment Summary</CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              <div className="p-4 rounded-lg bg-indigo-50 dark:bg-indigo-900/20 text-center">
                <p className="text-xs text-indigo-600 dark:text-indigo-400 font-medium">Total Due</p>
                <p className="text-2xl font-bold text-indigo-700 dark:text-indigo-300">₹1,21,000</p>
              </div>
              <div className="space-y-2 text-sm">
                <div className="flex justify-between">
                  <span className="text-slate-500">Paid</span>
                  <span className="font-medium text-emerald-600">₹0</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-500">Due Date</span>
                  <span className="font-medium text-slate-900 dark:text-white">Jun 30, 2026</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-500">Installments</span>
                  <span className="font-medium text-slate-900 dark:text-white">2 available</span>
                </div>
              </div>
              <Button className="w-full">
                <CreditCard className="w-4 h-4 mr-2" />
                Pay Full Amount
              </Button>
              <Button variant="outline" className="w-full">
                Pay 60% Installment
              </Button>
              <Button variant="ghost" size="sm" className="w-full text-xs">
                <Download className="w-3 h-3 mr-1" /> Download Fee Receipt
              </Button>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="text-sm">Scholarship Status</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="flex items-center gap-2 text-sm text-emerald-600 dark:text-emerald-400">
                <CheckCircle2 className="w-4 h-4" />
                Eligible for Post-Matric Scholarship
              </div>
              <p className="text-xs text-slate-500 mt-2">Apply through the scholarship portal within the first month.</p>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
    </AppShell>
  )
}
