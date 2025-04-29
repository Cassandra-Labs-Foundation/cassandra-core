import React, { useState } from 'react';
import { 
  CreditCard, 
  ArrowRight, 
  ArrowLeft,
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
  ChevronsUpDown,
  PlusCircle,
  MinusCircle,
  Receipt,
  Printer,
  CheckCircle,
  X,
  UserPlus,
  Eye
} from 'lucide-react';

export default function TellerModule() {
  const [activeTab, setActiveTab] = useState('teller');
  const [showMemberModal, setShowMemberModal] = useState(false);
  const [showTransactionModal, setShowTransactionModal] = useState(false);
  const [transactionType, setTransactionType] = useState('deposit');
  
  // Mock data
  const drawerBalance = {
    total: '$5,230.00',
    breakdown: [
      { denomination: '$100', count: 20, value: '$2,000.00' },
      { denomination: '$50', count: 14, value: '$700.00' },
      { denomination: '$20', count: 65, value: '$1,300.00' },
      { denomination: '$10', count: 48, value: '$480.00' },
      { denomination: '$5', count: 54, value: '$270.00' },
      { denomination: '$1', count: 180, value: '$180.00' },
      { denomination: 'Quarters', count: 100, value: '$25.00' },
      { denomination: 'Dimes', count: 350, value: '$35.00' },
      { denomination: 'Nickels', count: 480, value: '$24.00' },
      { denomination: 'Pennies', count: 1600, value: '$16.00' },
      { denomination: 'Checks', count: 4, value: '$2,140.50' }
    ],
    lastBalanced: 'Today, 8:15 AM'
  };
  
  const tellerJournal = [
    { id: 1, time: '2:34 PM', transaction: 'Deposit', member: 'James Wilson', amount: '+$1,250.00', receipt: '#423791', status: 'completed' },
    { id: 2, time: '1:47 PM', transaction: 'Withdrawal', member: 'Sarah Johnson', amount: '-$350.00', receipt: '#423790', status: 'completed' },
    { id: 3, time: '11:22 AM', transaction: 'Check Cashing', member: 'David Martinez', amount: '-$856.33', receipt: '#423789', status: 'completed' },
    { id: 4, time: '10:15 AM', transaction: 'Loan Payment', member: 'Mountain View LLC', amount: '-$2,430.15', receipt: '#423788', status: 'completed' },
    { id: 5, time: '9:05 AM', transaction: 'Cash Drawer Open', member: 'System', amount: '+$5,000.00', receipt: '#423787', status: 'completed' }
  ];
  
  const quickMembers = [
    { id: 1, name: 'James Wilson', accountNumber: '1001-5872', type: 'Basic Checking', balance: '$3,458.29', recent: true },
    { id: 2, name: 'Sarah Johnson', accountNumber: '1001-6932', type: 'Premier Savings', balance: '$12,843.59', recent: true },
    { id: 3, name: 'David Martinez', accountNumber: '1001-4387', type: 'Student Checking', balance: '$851.23', recent: true },
    { id: 4, name: 'Mountain View LLC', accountNumber: '1001-9932', type: 'Business Checking', balance: '$58,239.45', recent: false }
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
          
          <div className="hidden md:flex items-center space-x-4">
            <div className="flex items-center text-sm bg-green-100 text-green-800 px-3 py-1 rounded-md">
              <CheckCircle size={16} className="mr-1.5" />
              Drawer Balanced
            </div>
            <div className="flex items-center text-sm bg-blue-100 text-blue-800 px-3 py-1 rounded-md">
              <DollarSign size={16} className="mr-1.5" />
              {drawerBalance.total}
            </div>
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
        
        {/* Teller Dashboard */}
        <main className="flex-1 overflow-y-auto p-6">
          <div className="mb-6 flex justify-between items-center">
            <div className="flex items-center">
              <div className="mr-4">
                <h1 className="text-2xl font-semibold mb-1">Teller Dashboard</h1>
                <p className="text-slate-500">Tuesday, April 29, 2025</p>
              </div>
            </div>
            <div className="flex items-center space-x-3">
              <button 
                className="px-3 py-2 text-sm bg-white border border-slate-200 rounded-md hover:border-blue-500 flex items-center"
                onClick={() => setShowMemberModal(true)}
              >
                <UserPlus size={16} className="mr-1.5" />
                Find Member
              </button>
              <button 
                className="px-3 py-2 text-sm bg-blue-600 text-white rounded-md hover:bg-blue-700 flex items-center"
                onClick={() => {
                  setTransactionType('deposit');
                  setShowTransactionModal(true);
                }}
              >
                <PlusCircle size={16} className="mr-1.5" />
                New Transaction
              </button>
            </div>
          </div>
          
          {/* Two-column layout for larger screens */}
          <div className="flex flex-col md:flex-row gap-6">
            {/* Left column: Drawer Balance Card */}
            <div className="w-full md:w-1/3">
              <div className="bg-white rounded-lg border border-slate-200 overflow-hidden mb-6">
                <div className="flex justify-between items-center p-4 border-b border-slate-200">
                  <h2 className="font-semibold">Cash Drawer Balance</h2>
                  <div className="text-sm text-slate-500">Last balanced: {drawerBalance.lastBalanced}</div>
                </div>
                <div className="p-4">
                  <div className="flex justify-between items-center mb-4">
                    <div className="text-lg font-semibold text-slate-700">Total Cash</div>
                    <div className="text-2xl font-bold text-blue-600">{drawerBalance.total}</div>
                  </div>
                  
                  <div className="space-y-1 mb-4 max-h-60 overflow-y-auto">
                    {drawerBalance.breakdown.map((item, index) => (
                      <div key={index} className="flex justify-between items-center py-1.5 border-b border-slate-100 last:border-0">
                        <div className="flex items-center">
                          <span className="font-medium text-sm text-slate-700">{item.denomination}</span>
                          <span className="ml-2 text-xs text-slate-500">× {item.count}</span>
                        </div>
                        <div className="text-sm">{item.value}</div>
                      </div>
                    ))}
                  </div>
                </div>
                <div className="bg-slate-50 px-4 py-3 border-t border-slate-200 flex justify-between">
                  <button className="text-slate-600 text-sm font-medium flex items-center">
                    <Printer size={16} className="mr-1.5" />
                    Print
                  </button>
                  <button className="text-blue-600 text-sm font-medium flex items-center">
                    <RefreshCw size={16} className="mr-1.5" />
                    Balance Drawer
                  </button>
                </div>
              </div>
              
              {/* Quick Member Access */}
              <div className="bg-white rounded-lg border border-slate-200 overflow-hidden">
                <div className="flex justify-between items-center p-4 border-b border-slate-200">
                  <h2 className="font-semibold">Recent Members</h2>
                  <button className="text-blue-600 text-sm font-medium">View All</button>
                </div>
                <div className="divide-y divide-slate-100">
                  {quickMembers.map(member => (
                    <div key={member.id} className="p-3 hover:bg-slate-50">
                      <div className="flex justify-between mb-1">
                        <div className="font-medium">{member.name}</div>
                        {member.recent && (
                          <span className="text-xs bg-blue-100 text-blue-800 px-2 py-0.5 rounded-full">
                            Recent
                          </span>
                        )}
                      </div>
                      <div className="flex justify-between items-center">
                        <div className="text-xs text-slate-500">{member.accountNumber} • {member.type}</div>
                        <div className="text-sm font-medium">{member.balance}</div>
                      </div>
                      <div className="mt-2 flex space-x-2">
                        <button 
                          className="text-xs px-2 py-1 bg-slate-100 text-slate-600 rounded hover:bg-slate-200"
                          onClick={() => {
                            setTransactionType('deposit');
                            setShowTransactionModal(true);
                          }}
                        >
                          Deposit
                        </button>
                        <button 
                          className="text-xs px-2 py-1 bg-slate-100 text-slate-600 rounded hover:bg-slate-200"
                          onClick={() => {
                            setTransactionType('withdrawal');
                            setShowTransactionModal(true);
                          }}
                        >
                          Withdraw
                        </button>
                        <button 
                          className="text-xs px-2 py-1 bg-blue-50 text-blue-600 rounded hover:bg-blue-100"
                          onClick={() => setShowMemberModal(true)}
                        >
                          Details
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
                <div className="bg-slate-50 p-3 border-t border-slate-200 text-center">
                  <button className="text-blue-600 text-sm font-medium">
                    + Add New Member
                  </button>
                </div>
              </div>
            </div>
            
            {/* Right column: Transaction Journal */}
            <div className="w-full md:w-2/3">
              <div className="bg-white rounded-lg border border-slate-200 overflow-hidden">
                <div className="flex justify-between items-center p-4 border-b border-slate-200">
                  <h2 className="font-semibold">Transaction Journal</h2>
                  <div className="flex items-center space-x-2">
                    <div className="text-sm text-slate-500">Today's Total: +$2,613.52</div>
                    <button className="text-blue-600 text-sm font-medium flex items-center ml-4">
                      <Filter size={16} className="mr-1.5" />
                      Filter
                    </button>
                  </div>
                </div>
                <div className="overflow-x-auto">
                  <table className="w-full">
                    <thead>
                      <tr className="border-b border-slate-200 bg-slate-50">
                        <th className="text-left py-3 px-4 text-sm font-medium text-slate-500">Time</th>
                        <th className="text-left py-3 px-4 text-sm font-medium text-slate-500">Transaction</th>
                        <th className="text-left py-3 px-4 text-sm font-medium text-slate-500">Member</th>
                        <th className="text-left py-3 px-4 text-sm font-medium text-slate-500">Receipt #</th>
                        <th className="text-right py-3 px-4 text-sm font-medium text-slate-500">Amount</th>
                        <th className="text-right py-3 px-4 text-sm font-medium text-slate-500">Actions</th>
                      </tr>
                    </thead>
                    <tbody>
                      {tellerJournal.map(entry => (
                        <tr key={entry.id} className="border-b border-slate-200 last:border-b-0 hover:bg-slate-50">
                          <td className="py-3 px-4 text-sm">
                            <div className="flex items-center">
                              <Clock size={14} className="mr-1.5 text-slate-400" />
                              {entry.time}
                            </div>
                          </td>
                          <td className="py-3 px-4 text-sm">
                            <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                              entry.transaction === 'Deposit' ? 'bg-green-100 text-green-800' :
                              entry.transaction === 'Withdrawal' ? 'bg-orange-100 text-orange-800' :
                              entry.transaction === 'Loan Payment' ? 'bg-purple-100 text-purple-800' :
                              entry.transaction === 'Check Cashing' ? 'bg-yellow-100 text-yellow-800' :
                              'bg-blue-100 text-blue-800'
                            }`}>
                              {entry.transaction}
                            </span>
                          </td>
                          <td className="py-3 px-4">
                            <div className="font-medium text-sm">{entry.member}</div>
                          </td>
                          <td className="py-3 px-4 text-sm text-slate-500">
                            {entry.receipt}
                          </td>
                          <td className="py-3 px-4 text-right font-medium whitespace-nowrap">
                            <span className={entry.amount.startsWith('+') ? 'text-green-600' : 'text-slate-800'}>
                              {entry.amount}
                            </span>
                          </td>
                          <td className="py-3 px-4 text-right">
                            <div className="flex items-center justify-end space-x-2">
                              <button className="text-slate-400 hover:text-slate-600">
                                <Printer size={16} />
                              </button>
                              <button className="text-slate-400 hover:text-slate-600">
                                <Eye size={16} />
                              </button>
                              <button className="text-blue-600 text-sm font-medium">
                                Reverse
                              </button>
                            </div>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
                <div className="bg-slate-50 px-4 py-3 border-t border-slate-200 flex items-center justify-between">
                  <div className="text-sm text-slate-500">Showing today's transactions</div>
                  <div className="flex space-x-1">
                    <button className="px-3 py-1 border border-slate-300 rounded-md text-sm bg-white">Previous</button>
                    <button className="px-3 py-1 border border-blue-500 bg-blue-500 text-white rounded-md text-sm">Next</button>
                  </div>
                </div>
              </div>
              
              {/* Transaction Quick Actions */}
              <div className="grid grid-cols-3 gap-3 mt-6">
                <TransactionButton 
                  icon={<PlusCircle size={20} />} 
                  label="Deposit"
                  description="Cash or check deposit"
                  onClick={() => {
                    setTransactionType('deposit');
                    setShowTransactionModal(true);
                  }}
                />
                <TransactionButton 
                  icon={<MinusCircle size={20} />} 
                  label="Withdrawal"
                  description="Cash withdrawal"
                  onClick={() => {
                    setTransactionType('withdrawal');
                    setShowTransactionModal(true);
                  }}
                />
                <TransactionButton 
                  icon={<Receipt size={20} />} 
                  label="Check Cashing"
                  description="For members & non-members"
                  onClick={() => {
                    setTransactionType('check');
                    setShowTransactionModal(true);
                  }}
                />
              </div>
            </div>
          </div>
        </main>
      </div>
      
      {/* Member Quick Edit Modal */}
      {showMemberModal && (
        <div className="fixed inset-0 bg-slate-800/50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg shadow-xl w-full max-w-2xl">
            <div className="flex justify-between items-center p-4 border-b border-slate-200">
              <h2 className="font-semibold text-lg">Member Details</h2>
              <button 
                className="text-slate-400 hover:text-slate-600"
                onClick={() => setShowMemberModal(false)}
              >
                <X size={20} />
              </button>
            </div>
            <div className="p-6">
              <div className="flex items-start mb-6">
                <div className="w-16 h-16 rounded-full bg-blue-100 flex items-center justify-center text-blue-600 mr-4">
                  <User size={28} />
                </div>
                <div>
                  <h3 className="text-xl font-semibold mb-1">James Wilson</h3>
                  <div className="text-slate-500">Member since October 2020</div>
                  <div className="mt-2 flex space-x-2">
                    <span className="text-xs bg-green-100 text-green-800 px-2 py-0.5 rounded-full">
                      Good Standing
                    </span>
                    <span className="text-xs bg-blue-100 text-blue-800 px-2 py-0.5 rounded-full">
                      Direct Deposit
                    </span>
                  </div>
                </div>
              </div>
              
              {/* Account Summary */}
              <div className="mb-6">
                <h4 className="font-medium text-slate-800 mb-2">Accounts</h4>
                <div className="bg-slate-50 rounded-lg border border-slate-200 overflow-hidden">
                  <table className="w-full">
                    <thead>
                      <tr className="border-b border-slate-200">
                        <th className="text-left py-2 px-3 text-xs font-medium text-slate-500">Account Type</th>
                        <th className="text-left py-2 px-3 text-xs font-medium text-slate-500">Number</th>
                        <th className="text-right py-2 px-3 text-xs font-medium text-slate-500">Balance</th>
                        <th className="text-right py-2 px-3 text-xs font-medium text-slate-500">Available</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr className="border-b border-slate-200">
                        <td className="py-2 px-3 text-sm font-medium">Basic Checking</td>
                        <td className="py-2 px-3 text-sm text-slate-500">1001-5872</td>
                        <td className="py-2 px-3 text-sm text-right">$3,458.29</td>
                        <td className="py-2 px-3 text-sm text-right font-medium text-green-600">$3,458.29</td>
                      </tr>
                      <tr>
                        <td className="py-2 px-3 text-sm font-medium">Savings Account</td>
                        <td className="py-2 px-3 text-sm text-slate-500">1001-5873</td>
                        <td className="py-2 px-3 text-sm text-right">$12,587.63</td>
                        <td className="py-2 px-3 text-sm text-right font-medium text-green-600">$12,587.63</td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
              
              {/* Contact Information */}
              <div className="grid grid-cols-2 gap-4 mb-6">
                <div>
                  <h4 className="font-medium text-slate-800 mb-2">Contact Information</h4>
                  <div className="bg-slate-50 rounded-lg border border-slate-200 p-3">
                    <div className="mb-2">
                      <div className="text-xs text-slate-500">Email</div>
                      <div className="text-sm">james.wilson@example.com</div>
                    </div>
                    <div className="mb-2">
                      <div className="text-xs text-slate-500">Phone</div>
                      <div className="text-sm">(555) 123-4567</div>
                    </div>
                    <div>
                      <div className="text-xs text-slate-500">Address</div>
                      <div className="text-sm">123 Main Street, Apt 4B<br />Springfield, CA 94321</div>
                    </div>
                  </div>
                </div>
                
                <div>
                  <h4 className="font-medium text-slate-800 mb-2">Member Notes</h4>
                  <div className="bg-slate-50 rounded-lg border border-slate-200 p-3 h-32 overflow-y-auto">
                    <div className="text-sm">
                      <p className="mb-2">Prefers email communication. Called about setting up direct deposit on 4/15/2025.</p>
                      <p>Interested in auto loan options for summer 2025.</p>
                    </div>
                  </div>
                </div>
              </div>
              
              {/* Action Buttons */}
              <div className="flex justify-between">
                <div className="space-x-2">
                  <button className="px-3 py-1.5 text-sm border border-slate-200 rounded-md hover:border-slate-300 text-slate-600">
                    Edit Details
                  </button>
                  <button className="px-3 py-1.5 text-sm border border-slate-200 rounded-md hover:border-slate-300 text-slate-600">
                    View History
                  </button>
                </div>
                <div className="space-x-2">
                  <button className="px-3 py-1.5 text-sm border border-blue-500 bg-blue-50 rounded-md hover:bg-blue-100 text-blue-600"
                    onClick={() => {
                      setShowMemberModal(false);
                      setTransactionType('deposit');
                      setShowTransactionModal(true);
                    }}
                  >
                    New Transaction
                  </button>
                  <button className="px-3 py-1.5 text-sm bg-blue-600 text-white rounded-md hover:bg-blue-700"
                    onClick={() => setShowMemberModal(false)}
                  >
                    Save & Close
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
      
      {/* Transaction Modal */}
      {showTransactionModal && (
        <div className="fixed inset-0 bg-slate-800/50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg shadow-xl w-full max-w-xl">
            <div className="flex justify-between items-center p-4 border-b border-slate-200">
              <h2 className="font-semibold text-lg">
                {transactionType === 'deposit' ? 'New Deposit' : 
                 transactionType === 'withdrawal' ? 'New Withdrawal' : 
                 'Check Cashing'}
              </h2>
              <button 
                className="text-slate-400 hover:text-slate-600"
                onClick={() => setShowTransactionModal(false)}
              >
                <X size={20} />
              </button>
            </div>
            <div className="p-6">
              {/* Member Selection */}
              <div className="mb-4">
                <label className="block text-sm font-medium text-slate-700 mb-2">Member</label>
                <div className="relative">
                  <Search size={18} className="absolute left-3 top-1/2 transform -translate-y-1/2 text-slate-400" />
                  <input 
                    type="text" 
                    placeholder="Search by name or account number..."
                    className="pl-10 pr-4 py-2 bg-slate-50 border border-slate-200 rounded-md w-full focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm"
                    defaultValue="James Wilson (1001-5872)"
                  />
                </div>
              </div>
              
              {/* Account Selection */}
              <div className="mb-4">
                <label className="block text-sm font-medium text-slate-700 mb-2">Account</label>
                <select className="w-full border border-slate-200 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm">
                  <option value="checking">Basic Checking (1001-5872)</option>
                  <option value="savings">Savings Account (1001-5873)</option>
                </select>
              </div>
              
              {/* Transaction Amount */}
              <div className="mb-4">
                <label className="block text-sm font-medium text-slate-700 mb-2">Amount</label>
                <div className="relative">
                  <div className="absolute left-3 top-1/2 transform -translate-y-1/2 text-slate-400">$</div>
                  <input 
                    type="text" 
                    className="pl-8 pr-4 py-2 bg-slate-50 border border-slate-200 rounded-md w-full focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm"
                    placeholder="0.00"
                  />
                </div>
              </div>
              
              {/* Transaction Details */}
              <div className="mb-4">
                <label className="block text-sm font-medium text-slate-700 mb-2">Transaction Details</label>
                <textarea 
                  className="w-full h-24 p-3 bg-slate-50 border border-slate-200 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm"
                  placeholder="Enter any notes or transaction details..."
                ></textarea>
              </div>
              
              {transactionType === 'deposit' && (
                <div className="mb-4">
                  <label className="block text-sm font-medium text-slate-700 mb-2">Deposit Type</label>
                  <div className="flex space-x-4">
                    <label className="flex items-center">
                      <input type="radio" name="depositType" className="mr-2" defaultChecked />
                      <span className="text-sm">Cash</span>
                    </label>
                    <label className="flex items-center">
                      <input type="radio" name="depositType" className="mr-2" />
                      <span className="text-sm">Check</span>
                    </label>
                    <label className="flex items-center">
                      <input type="radio" name="depositType" className="mr-2" />
                      <span className="text-sm">Mixed</span>
                    </label>
                  </div>
                </div>
              )}
              
              {transactionType === 'withdrawal' && (
                <div className="mb-4">
                  <label className="block text-sm font-medium text-slate-700 mb-2">Cash Denomination</label>
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <label className="flex items-center justify-between mb-2">
                        <span className="text-sm">$100 bills:</span>
                        <input type="number" className="w-16 p-1 border border-slate-200 rounded" />
                      </label>
                      <label className="flex items-center justify-between mb-2">
                        <span className="text-sm">$50 bills:</span>
                        <input type="number" className="w-16 p-1 border border-slate-200 rounded" />
                      </label>
                      <label className="flex items-center justify-between mb-2">
                        <span className="text-sm">$20 bills:</span>
                        <input type="number" className="w-16 p-1 border border-slate-200 rounded" />
                      </label>
                    </div>
                    <div>
                      <label className="flex items-center justify-between mb-2">
                        <span className="text-sm">$10 bills:</span>
                        <input type="number" className="w-16 p-1 border border-slate-200 rounded" />
                      </label>
                      <label className="flex items-center justify-between mb-2">
                        <span className="text-sm">$5 bills:</span>
                        <input type="number" className="w-16 p-1 border border-slate-200 rounded" />
                      </label>
                      <label className="flex items-center justify-between mb-2">
                        <span className="text-sm">$1 bills:</span>
                        <input type="number" className="w-16 p-1 border border-slate-200 rounded" />
                      </label>
                    </div>
                  </div>
                </div>
              )}
              
              {transactionType === 'check' && (
                <div className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-slate-700 mb-2">Check Number</label>
                    <input 
                      type="text" 
                      className="px-3 py-2 bg-slate-50 border border-slate-200 rounded-md w-full focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm"
                      placeholder="Enter check number..."
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-slate-700 mb-2">Check Date</label>
                    <input 
                      type="date" 
                      className="px-3 py-2 bg-slate-50 border border-slate-200 rounded-md w-full focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-slate-700 mb-2">ID Verification</label>
                    <select className="w-full border border-slate-200 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm">
                      <option value="drivers">Driver's License</option>
                      <option value="state">State ID</option>
                      <option value="passport">Passport</option>
                      <option value="military">Military ID</option>
                    </select>
                  </div>
                </div>
              )}
              
              <div className="mt-6 flex justify-end space-x-3">
                <button 
                  className="px-4 py-2 border border-slate-200 rounded-md text-slate-600 hover:border-slate-300"
                  onClick={() => setShowTransactionModal(false)}
                >
                  Cancel
                </button>
                <button 
                  className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
                  onClick={() => setShowTransactionModal(false)}
                >
                  Complete Transaction
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

// Navigation Item Component
function NavItem({ icon, label, active, onClick }) {
  return (
    <li className="mb-1">
      <button
        onClick={onClick}
        className={`flex items-center w-full py-2.5 px-4 rounded-md ${
          active 
            ? 'bg-blue-50 text-blue-600' 
            : 'text-slate-600 hover:bg-slate-100'
        }`}
      >
        <span className="mr-3">{icon}</span>
        <span className="hidden md:block font-medium text-sm">{label}</span>
      </button>
    </li>
  );
}

// Transaction Button Component
function TransactionButton({ icon, label, description, onClick }) {
  return (
    <button 
      onClick={onClick}
      className="flex flex-col items-center p-4 bg-white border border-slate-200 rounded-lg hover:border-blue-500 hover:shadow-sm transition-all"
    >
      <div className="w-12 h-12 rounded-full bg-blue-50 flex items-center justify-center text-blue-600 mb-2">
        {icon}
      </div>
      <div className="font-medium text-slate-800">{label}</div>
      <div className="text-xs text-slate-500 text-center mt-1">{description}</div>
    </button>
  );
}