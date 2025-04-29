// src/components/dashboard/Dashboard.jsx
import React, { useState } from 'react';
import {
  CreditCard,
  ArrowRight,
  Search,
  Bell,
  Settings,
  User,
  DollarSign,
  BarChart2,
  Users,
  FileText,
  Shield,
  Grid,
  Filter,
  Download,
  Calendar,
  Clock,
  Book,
  Link,
  RefreshCw,
  HelpCircle,
} from 'lucide-react';

export default function MercuryDashboard() {
  const [activeTab, setActiveTab] = useState('home');
  const [showFilters, setShowFilters] = useState(false);

  // Mock data
  const accounts = [
    { id: 1, name: 'Main Credit Union Account', balance: '$58,239.45', type: 'checking' },
    { id: 2, name: 'Business Savings', balance: '$125,873.21', type: 'savings' },
    { id: 3, name: 'Member Loan Fund', balance: '$432,950.00', type: 'loan' },
  ];

  const recentTransactions = [
    { id: 1, member: 'James Wilson', type: 'Deposit', amount: '+$1,250.00', date: 'Today, 2:34 PM', status: 'completed', category: 'Deposit' },
    { id: 2, member: 'Sarah Johnson', type: 'Withdrawal', amount: '-$350.00', date: 'Today, 11:15 AM', status: 'completed', category: 'Member Service' },
    { id: 3, member: 'Mountain View LLC', type: 'Loan Payment', amount: '-$2,430.15', date: 'Yesterday', status: 'completed', category: 'Loan' },
    { id: 4, member: 'Robert Chen', type: 'Transfer', amount: '-$500.00', date: 'Yesterday', status: 'pending', category: 'Transfer' },
    { id: 5, member: 'Emma Garcia', type: 'Fee', amount: '-$25.00', date: 'Apr 28, 2025', status: 'completed', category: 'Fee' },
    { id: 6, member: 'Northwest Credit Union', type: 'ACH Transfer', amount: '-$756.33', date: 'Apr 27, 2025', status: 'completed', category: 'Shared Branch' },
  ];

  const quickActions = [
    { id: 1, name: 'New Member', icon: <Users size={20} /> },
    { id: 2, name: 'Process Loan', icon: <FileText size={20} /> },
    { id: 3, name: 'Cash Drawer', icon: <DollarSign size={20} /> },
    { id: 4, name: 'Reports', icon: <BarChart2 size={20} /> },
  ];

  const categories = [
    'All Categories',
    'Deposit',
    'Withdrawal',
    'Loan',
    'Transfer',
    'Fee',
    'Member Service',
    'Shared Branch',
    'Uncategorized',
  ];

  return (
    <div className="flex h-screen bg-slate-50 text-slate-800 overflow-hidden">
      {/* Left Sidebar */}
      <div className="w-16 md:w-64 bg-white border-r border-slate-200 flex flex-col">
        <div className="p-4 border-b border-slate-200">
          <div className="font-bold text-xl hidden md:block">Pynthia Banking</div>
          <div className="md:hidden flex justify-center">
            <Shield size={24} className="text-blue-600" />
          </div>
        </div>

        <nav className="flex-1 py-6">
          <ul>
            <NavItem
              icon={<Grid size={20} />}
              label="Home"
              active={activeTab === 'home'}
              onClick={() => setActiveTab('home')}
            />
            <NavItem
              icon={<DollarSign size={20} />}
              label="Teller"
              active={activeTab === 'teller'}
              onClick={() => setActiveTab('teller')}
            />
            <NavItem
              icon={<Users size={20} />}
              label="Member Services"
              active={activeTab === 'members'}
              onClick={() => setActiveTab('members')}
            />
            <NavItem
              icon={<FileText size={20} />}
              label="Lending"
              active={activeTab === 'lending'}
              onClick={() => setActiveTab('lending')}
            />
            <NavItem
              icon={<BarChart2 size={20} />}
              label="Accounting"
              active={activeTab === 'accounting'}
              onClick={() => setActiveTab('accounting')}
            />
            <NavItem
              icon={<Book size={20} />}
              label="Reports"
              active={activeTab === 'reports'}
              onClick={() => setActiveTab('reports')}
            />
            <NavItem
              icon={<Link size={20} />}
              label="API"
              active={activeTab === 'api'}
              onClick={() => setActiveTab('api')}
            />
            <NavItem
              icon={<Shield size={20} />}
              label="Admin"
              active={activeTab === 'admin'}
              onClick={() => setActiveTab('admin')}
            />
          </ul>
        </nav>

        <div className="p-4 border-t border-slate-200">
          <div className="flex items-center space-x-3">
            <div className="w-8 h-8 rounded-full bg-blue-600 flex items-center justify-center text-white">
              <User size={16} />
            </div>
            <div className="hidden md:block">
              <div className="font-semibold text-sm">Sarah Thompson</div>
              <div className="text-xs text-slate-500">Teller</div>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Top Header */}
        <header className="h-16 bg-white border-b border-slate-200 flex items-center justify-between px-6">
          <div className="flex items-center space-x-3 w-1/3">
            <div className="relative flex-grow">
              <Search size={18} className="absolute left-3 top-1/2 transform -translate-y-1/2 text-slate-400" />
              <input
                type="text"
                placeholder="Search members, accounts, or type / for commands..."
                className="pl-10 pr-4 py-2 bg-slate-100 rounded-md w-full max-w-md focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm"
              />
            </div>
          </div>

          <div className="hidden md:flex items-center space-x-1">
            <button className="px-3 py-1.5 text-sm rounded-md hover:bg-slate-100">Accounting</button>
            <button className="px-3 py-1.5 text-sm rounded-md hover:bg-slate-100">Treasury</button>
            <button className="px-3 py-1.5 text-sm rounded-md hover:bg-slate-100">Cards</button>
            <button className="px-3 py-1.5 text-sm rounded-md hover:bg-slate-100">API</button>
          </div>

          <div className="flex items-center space-x-4">
            <button className="text-slate-600 hover:text-slate-900 relative">
              <Bell size={20} />
              <span className="absolute top-0 right-0 w-2 h-2 bg-red-500 rounded-full"></span>
            </button>
            <button className="text-slate-600 hover:text-slate-900">
              <Settings size={20} />
            </button>
          </div>
        </header>

        {/* Dashboard Content */}
        <main className="flex-1 overflow-y-auto p-6">
          <div className="mb-6 flex justify-between items-start">
            <div>
              <h1 className="text-2xl font-semibold mb-2">Dashboard</h1>
              <p className="text-slate-500">Welcome back, Sarah. Here's what's happening today.</p>
            </div>
            <div className="flex items-center space-x-3">
              <button className="px-3 py-2 text-sm bg-white border border-slate-200 rounded-md hover:border-blue-500 flex items-center">
                <Download size={16} className="mr-1.5" />
                Export Data
              </button>
              <button className="px-3 py-2 text-sm bg-blue-600 text-white rounded-md hover:bg-blue-700 flex items-center">
                <DollarSign size={16} className="mr-1.5" />
                New Transaction
              </button>
            </div>
          </div>

          {/* System Alert */}
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-3 mb-6 flex items-center">
            <div className="w-10 h-10 rounded-full bg-blue-100 flex items-center justify-center mr-3">
              <Bell size={18} className="text-blue-600" />
            </div>
            <div className="flex-1">
              <h3 className="font-medium text-blue-800">System Maintenance Scheduled</h3>
              <p className="text-sm text-blue-600">A system update is scheduled for May 5, 2025, from 2:00 AM to 4:00 AM ET.</p>
            </div>
            <button className="text-blue-600 px-3 py-1 text-sm">Dismiss</button>
          </div>

          {/* Quick Action Cards */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
            {quickActions.map(action => (
              <button
                key={action.id}
                className="bg-white rounded-lg p-4 border border-slate-200 hover:border-blue-500 hover:shadow-sm transition-all flex flex-col items-center justify-center h-24"
              >
                <div className="w-10 h-10 rounded-full bg-blue-50 flex items-center justify-center text-blue-600 mb-2">
                  {action.icon}
                </div>
                <span className="text-sm font-medium">{action.name}</span>
              </button>
            ))}
          </div>

          {/* Accounts Section */}
          <div className="mb-8">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-lg font-semibold">Accounts</h2>
              <div className="flex items-center space-x-3">
                <button className="px-3 py-1.5 text-sm rounded-md bg-blue-600 text-white hover:bg-blue-700">
                  + New Account
                </button>
                <button className="text-blue-600 text-sm font-medium flex items-center">
                  View all <ArrowRight size={16} className="ml-1" />
                </button>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {accounts.map(account => (
                <div key={account.id} className="bg-white rounded-lg border border-slate-200 overflow-hidden hover:border-blue-300 hover:shadow-sm transition-all">
                  <div className="p-4">
                    <div className="flex justify-between items-start mb-3">
                      <div className="flex items-center">
                        <span className={`inline-block w-3 h-3 rounded-full mr-2 ${
                          account.type === 'loan' ? 'bg-purple-500' :
                          account.type === 'savings' ? 'bg-green-500' :
                          'bg-blue-500'
                        }`}></span>
                        <div className="text-sm text-slate-500 capitalize">{account.type === 'loan' ? 'Loan Fund' : account.type === 'savings' ? 'Savings' : 'Checking'}</div>
                      </div>
                      <CreditCard size={18} className="text-slate-400" />
                    </div>
                    <div className="font-semibold text-xl mb-2">{account.balance}</div>
                    <div className="text-sm truncate text-slate-700">{account.name}</div>
                  </div>
                  <div className="flex border-t border-slate-200">
                    <button className="flex-1 text-center py-2.5 text-sm font-medium text-blue-600 hover:bg-blue-50 border-r border-slate-200">
                      Transfer
                    </button>
                    <button className="flex-1 text-center py-2.5 text-sm font-medium text-blue-600 hover:bg-blue-50">
                      View Details
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Recent Transactions */}
          <div>
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-lg font-semibold">Recent Transactions</h2>
              <div className="flex items-center space-x-2">
                <button
                  onClick={() => setShowFilters(!showFilters)}
                  className="flex items-center text-slate-600 bg-white border border-slate-200 rounded-md px-3 py-1.5 text-sm hover:border-blue-500"
                >
                  <Filter size={16} className="mr-1.5" />
                  Filter
                </button>
                <button className="flex items-center text-slate-600 bg-white border border-slate-200 rounded-md px-3 py-1.5 text-sm hover:border-blue-500">
                  <Download size={16} className="mr-1.5" />
                  Export
                </button>
                <button className="text-blue-600 text-sm font-medium flex items-center ml-2">
                  View all <ArrowRight size={16} className="ml-1" />
                </button>
              </div>
            </div>

            {showFilters && (
              <div className="bg-white rounded-lg border border-slate-200 p-4 mb-4 grid grid-cols-1 md:grid-cols-3 gap-4">
                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-1">Category</label>
                  <select className="w-full border border-slate-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm">
                    {categories.map((category, index) => (
                      <option key={index} value={category}>{category}</option>
                    ))}
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-1">Date Range</label>
                  <div className="flex items-center border border-slate-300 rounded-md overflow-hidden">
                    <div className="px-3 py-2 bg-slate-50 text-slate-500">
                      <Calendar size={16} />
                    </div>
                    <select className="w-full border-0 focus:outline-none focus:ring-0 text-sm py-2">
                      <option value="today">Today</option>
                      <option value="yesterday">Yesterday</option>
                      <option value="this_week">This Week</option>
                      <option value="last_week">Last Week</option>
                      <option value="this_month">This Month</option>
                      <option value="last_month">Last Month</option>
                      <option value="custom">Custom Range</option>
                    </select>
                  </div>
                </div>
                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-1">Status</label>
                  <select className="w-full border border-slate-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm">
                    <option value="all">All Statuses</option>
                    <option value="completed">Completed</option>
                    <option value="pending">Pending</option>
                    <option value="failed">Failed</option>
                  </select>
                </div>
              </div>
            )}

            <div className="bg-white rounded-lg border border-slate-200 overflow-hidden">
              <table className="w-full">
                <thead>
                  <tr className="border-b border-slate-200 bg-slate-50">
                    <th className="text-left py-3 px-4 text-sm font-medium text-slate-500">Member</th>
                    <th className="text-left py-3 px-4 text-sm font-medium text-slate-500">Type</th>
                    <th className="text-left py-3 px-4 text-sm font-medium text-slate-500">Category</th>
                    <th className="text-left py-3 px-4 text-sm font-medium text-slate-500">Date</th>
                    <th className="text-right py-3 px-4 text-sm font-medium text-slate-500">Amount</th>
                    <th className="text-right py-3 px-4 text-sm font-medium text-slate-500">Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {recentTransactions.map(transaction => (
                    <tr key={transaction.id} className="border-b border-slate-200 last:border-b-0 hover:bg-slate-50">
                      <td className="py-3 px-4">
                        <div className="font-medium">{transaction.member}</div>
                      </td>
                      <td className="py-3 px-4 text-sm">{transaction.type}</td>
                      <td className="py-3 px-4 text-sm">
                        <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-50 text-blue-800">
                          {transaction.category}
                        </span>
                      </td>
                      <td className="py-3 px-4 text-sm text-slate-500 whitespace-nowrap">
                        <div className="flex items-center">
                          <Clock size={14} className="mr-1.5 text-slate-400" />
                          {transaction.date}
                        </div>
                      </td>
                      <td className="py-3 px-4 text-right font-medium whitespace-nowrap">
                        <span className={transaction.amount.startsWith('+') ? 'text-green-600' : 'text-slate-800'}>
                          {transaction.amount}
                        </span>
                        {transaction.status === 'pending' && (
                          <span className="ml-2 text-xs font-medium bg-yellow-100 text-yellow-800 py-0.5 px-1.5 rounded">Pending</span>
                        )}
                      </td>
                      <td className="py-3 px-4 text-right">
                        <button className="text-blue-600 text-sm font-medium hover:text-blue-800">Details</button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
              <div className="bg-slate-50 px-4 py-3 border-t border-slate-200 flex items-center justify-between">
                <div className="text-sm text-slate-500">Showing 6 of 243 transactions</div>
                <div className="flex space-x-1">
                  <button className="px-3 py-1 border border-slate-300 rounded-md text-sm bg-white">Previous</button>
                  <button className="px-3 py-1 border border-blue-500 bg-blue-500 text-white rounded-md text-sm">Next</button>
                </div>
              </div>
            </div>
          </div>

          {/* Footer Help Section */}
          <div className="mt-8 pt-6 border-t border-slate-200">
            <div className="flex justify-between items-center">
              <div className="flex items-center space-x-8">
                <button className="flex items-center text-slate-600 hover:text-blue-600">
                  <HelpCircle size={18} className="mr-2" />
                  <span className="text-sm">Help Center</span>
                </button>
                <button className="flex items-center text-slate-600 hover:text-blue-600">
                  <RefreshCw size={18} className="mr-2" />
                  <span className="text-sm">Sync Accounts</span>
                </button>
              </div>
              <div>
                <span className="text-xs text-slate-500">Last updated: Today at 3:45 PM</span>
              </div>
            </div>
          </div>
        </main>
      </div>

      {/* Right Sidebar - Quick Access Panel */}
      <div className="hidden lg:block w-80 border-l border-slate-200 bg-white p-4 overflow-y-auto">
        <div className="mb-6">
          <h3 className="text-sm font-semibold text-slate-500 mb-3 uppercase">Quick Access</h3>
          <div className="space-y-2">
            <QuickAccessButton label="Find Member" icon={<Users size={16} />} />
            <QuickAccessButton label="Teller Drawer" icon={<DollarSign size={16} />} />
            <QuickAccessButton label="New Loan Application" icon={<FileText size={16} />} />
            <QuickAccessButton label="Transfer Funds" icon={<RefreshCw size={16} />} />
          </div>
        </div>

        <div className="mb-6">
          <h3 className="text-sm font-semibold text-slate-500 mb-3 uppercase">System Status</h3>
          <div className="bg-green-50 rounded-md p-3 border border-green-200 mb-2">
            <div className="flex items-center">
              <div className="w-2 h-2 rounded-full bg-green-500 mr-2"></div>
              <span className="text-sm text-green-800">All systems operational</span>
            </div>
          </div>
          <div className="text-xs text-slate-500">Next maintenance: May 5, 2025</div>
        </div>

        <div className="mb-6">
          <h3 className="text-sm font-semibold text-slate-500 mb-3 uppercase">Recent Activity</h3>
          <div className="space-y-3">
            <ActivityItem
              title="New member account created"
              description="James Wilson - Checking Account"
              time="10 minutes ago"
            />
            <ActivityItem
              title="Loan payment processed"
              description="Mountain View LLC - #123456"
              time="1 hour ago"
            />
            <ActivityItem
              title="Transfer completed"
              description="Robert Chen - Internal transfer"
              time="Yesterday"
            />
          </div>
        </div>

        <div>
          <h3 className="text-sm font-semibold text-slate-500 mb-3 uppercase">Core Integration</h3>
          <div className="bg-white rounded-md p-3 border border-slate-200">
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm font-medium">CU*Answers</span>
              <span className="text-xs px-2 py-0.5 bg-blue-100 text-blue-800 rounded-full">Connected</span>
            </div>
            <div className="text-xs text-slate-500 mb-2">Last sync: Today at 3:00 PM</div>
            <button className="w-full text-center py-1.5 text-xs font-medium text-blue-600 hover:bg-blue-50 rounded border border-blue-200">
              Force Sync
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

function NavItem({ icon, label, active, onClick }) {
  return (
    <li className="mb-1">
      <button
        onClick={onClick}
        className={`flex items-center w-full py-2.5 px-4 rounded-md ${
          active ? 'bg-blue-50 text-blue-600' : 'text-slate-600 hover:bg-slate-100'
        }`}
      >
        <span className="mr-3">{icon}</span>
        <span className="hidden md:block font-medium text-sm">{label}</span>
      </button>
    </li>
  );
}

function QuickAccessButton({ label, icon }) {
  return (
    <button className="flex items-center w-full px-3 py-2 rounded-md hover:bg-slate-100 text-slate-800">
      <span className="w-6 h-6 rounded flex items-center justify-center bg-blue-50 text-blue-500 mr-3">
        {icon}
      </span>
      <span className="text-sm">{label}</span>
    </button>
  );
}

function ActivityItem({ title, description, time }) {
  return (
    <div className="border-l-2 border-blue-400 pl-3">
      <div className="text-sm font-medium">{title}</div>
      <div className="text-xs text-slate-500">{description}</div>
      <div className="text-xs text-slate-400 mt-1">{time}</div>
    </div>
  );
}