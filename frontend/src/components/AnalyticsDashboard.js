import React, { useState, useEffect, useMemo } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Badge } from './ui/badge';
import { Button } from './ui/button';
import { 
  BarChart3, 
  PieChart, 
  TrendingUp, 
  Users, 
  Clock, 
  CheckCircle, 
  AlertCircle,
  Archive,
  Calendar,
  Star,
  Activity,
  Filter,
  Download
} from 'lucide-react';

const AnalyticsDashboard = ({ serviceRequests = [], contactMessages = [], testimonials = [] }) => {
  const [timeFilter, setTimeFilter] = useState('all'); // all, week, month, year
  const [selectedMetric, setSelectedMetric] = useState('requests');

  // Debug logging
  console.log('📊 Analytics Dashboard - Service Requests:', serviceRequests.length);
  console.log('📊 Analytics Dashboard - Approved Requests:', serviceRequests.filter(r => r.approved_for_kanban).length);
  console.log('📊 Analytics Dashboard - All Data:', serviceRequests);

  // Calculate key metrics
  const analytics = useMemo(() => {
    const now = new Date();
    const weekAgo = new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000);
    const monthAgo = new Date(now.getTime() - 30 * 24 * 60 * 60 * 1000);
    const yearAgo = new Date(now.getTime() - 365 * 24 * 60 * 60 * 1000);

    // Filter by time
    const filterByTime = (items) => {
      if (timeFilter === 'all') return items;
      
      const filterDate = timeFilter === 'week' ? weekAgo : 
                        timeFilter === 'month' ? monthAgo : yearAgo;
      
      return items.filter(item => new Date(item.created_at) >= filterDate);
    };

    const filteredRequests = filterByTime(serviceRequests);
    const filteredContacts = filterByTime(contactMessages);
    const filteredTestimonials = filterByTime(testimonials);

    // Service requests analytics
    const statusCounts = filteredRequests.reduce((acc, req) => {
      acc[req.status] = (acc[req.status] || 0) + 1;
      return acc;
    }, {});

    const deviceCounts = filteredRequests.reduce((acc, req) => {
      acc[req.device_type] = (acc[req.device_type] || 0) + 1;
      return acc;
    }, {});

    const urgencyCounts = filteredRequests.reduce((acc, req) => {
      acc[req.urgency] = (acc[req.urgency] || 0) + 1;
      return acc;
    }, {});

    // Revenue estimation
    const totalRevenue = filteredRequests
      .filter(req => req.price)
      .reduce((sum, req) => sum + parseFloat(req.price), 0);

    const averagePrice = filteredRequests.length > 0 ? 
      totalRevenue / filteredRequests.filter(req => req.price).length : 0;

    // Completion rate
    const completedRequests = filteredRequests.filter(req => 
      req.status === 'completed' || req.status === 'picked_up'
    ).length;
    const completionRate = filteredRequests.length > 0 ? 
      (completedRequests / filteredRequests.length) * 100 : 0;

    // Average rating
    const averageRating = filteredTestimonials.length > 0 ?
      filteredTestimonials.reduce((sum, t) => sum + t.rating, 0) / filteredTestimonials.length : 0;

    return {
      totalRequests: filteredRequests.length,
      totalContacts: filteredContacts.length,
      totalTestimonials: filteredTestimonials.length,
      statusCounts,
      deviceCounts,
      urgencyCounts,
      totalRevenue,
      averagePrice,
      completionRate,
      averageRating,
      completedRequests
    };
  }, [serviceRequests, contactMessages, testimonials, timeFilter]);

  // Chart data for status distribution
  const statusData = Object.entries(analytics.statusCounts).map(([status, count]) => ({
    name: getStatusLabel(status),
    value: count,
    color: getStatusColor(status)
  }));

  // Chart data for device types
  const deviceData = Object.entries(analytics.deviceCounts).map(([device, count]) => ({
    name: device.toUpperCase(),
    value: count,
    color: getDeviceColor(device)
  }));

  function getStatusLabel(status) {
    const labels = {
      'pending': 'მოლოდინი',
      'in_progress': 'მუშაობა',
      'completed': 'დასრულებული',
      'picked_up': 'გატანილი',
      'archived': 'არქივი'
    };
    return labels[status] || status;
  }

  function getStatusColor(status) {
    const colors = {
      'pending': '#fbbf24',
      'in_progress': '#3b82f6',
      'completed': '#10b981',
      'picked_up': '#8b5cf6',
      'archived': '#6b7280'
    };
    return colors[status] || '#6b7280';
  }

  function getDeviceColor(device) {
    const colors = {
      'hdd': '#ef4444',
      'ssd': '#3b82f6',
      'raid': '#8b5cf6',
      'usb': '#f59e0b',
      'sd': '#10b981',
      'other': '#6b7280'
    };
    return colors[device] || '#6b7280';
  }

  // Simple Bar Chart Component
  const SimpleBarChart = ({ data, title }) => {
    const maxValue = Math.max(...data.map(d => d.value));
    
    return (
      <div className="space-y-3">
        <h4 className="font-medium text-sm text-gray-300">{title}</h4>
        {data.map((item, index) => (
          <div key={index} className="space-y-1">
            <div className="flex justify-between text-sm">
              <span className="text-gray-300">{item.name}</span>
              <span className="text-white font-medium">{item.value}</span>
            </div>
            <div className="w-full bg-gray-700 rounded-full h-2">
              <div 
                className="h-2 rounded-full transition-all duration-300"
                style={{ 
                  width: `${(item.value / maxValue) * 100}%`,
                  backgroundColor: item.color 
                }}
              />
            </div>
          </div>
        ))}
      </div>
    );
  };

  // Donut Chart Component
  const SimpleDonutChart = ({ data, title }) => {
    const total = data.reduce((sum, d) => sum + d.value, 0);
    
    return (
      <div className="space-y-4">
        <h4 className="font-medium text-sm text-gray-300">{title}</h4>
        <div className="flex flex-col space-y-2">
          {data.map((item, index) => {
            const percentage = total > 0 ? ((item.value / total) * 100).toFixed(1) : 0;
            return (
              <div key={index} className="flex items-center justify-between">
                <div className="flex items-center space-x-2">
                  <div 
                    className="w-3 h-3 rounded-full"
                    style={{ backgroundColor: item.color }}
                  />
                  <span className="text-sm text-gray-300">{item.name}</span>
                </div>
                <div className="text-right">
                  <div className="text-sm font-medium text-white">{item.value}</div>
                  <div className="text-xs text-gray-400">{percentage}%</div>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    );
  };

  return (
    <div className="space-y-6 p-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-2xl font-bold text-white flex items-center gap-2">
            <Activity className="w-6 h-6 text-red-500" />
            Analytics Dashboard
          </h2>
          <p className="text-gray-400 mt-1">მონაცემთა ანალიზი და სტატისტიკა</p>
        </div>
        
        {/* Time Filter */}
        <div className="flex items-center space-x-2">
          <Filter className="w-4 h-4 text-gray-400" />
          <select 
            value={timeFilter}
            onChange={(e) => setTimeFilter(e.target.value)}
            className="bg-gray-800 border border-gray-700 rounded-md px-3 py-1 text-white text-sm"
          >
            <option value="all">ყველა დრო</option>
            <option value="week">ბოლო კვირა</option>
            <option value="month">ბოლო თვე</option>
            <option value="year">ბოლო წელი</option>
          </select>
        </div>
      </div>

      {/* Key Metrics Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <Card className="bg-gray-800 border-gray-700">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-gray-300">
              სულ მოთხოვნები
            </CardTitle>
            <Users className="h-4 w-4 text-blue-400" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-white">{analytics.totalRequests}</div>
            <p className="text-xs text-gray-400">
              დასრულებული: {analytics.completedRequests}
            </p>
          </CardContent>
        </Card>

        <Card className="bg-gray-800 border-gray-700">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-gray-300">
              დასრულების %
            </CardTitle>
            <CheckCircle className="h-4 w-4 text-green-400" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-white">
              {analytics.completionRate.toFixed(1)}%
            </div>
            <p className="text-xs text-gray-400">
              წარმატების ნაჩვენები
            </p>
          </CardContent>
        </Card>

        <Card className="bg-gray-800 border-gray-700">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-gray-300">
              საშუალო შეფასება
            </CardTitle>
            <Star className="h-4 w-4 text-yellow-400" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-white">
              {analytics.averageRating.toFixed(1)}/5
            </div>
            <p className="text-xs text-gray-400">
              {analytics.totalTestimonials} გამოხმაურება
            </p>
          </CardContent>
        </Card>

        <Card className="bg-gray-800 border-gray-700">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-gray-300">
              სულ შემოსავალი
            </CardTitle>
            <TrendingUp className="h-4 w-4 text-green-400" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-white">
              {analytics.totalRevenue.toFixed(0)}₾
            </div>
            <p className="text-xs text-gray-400">
              საშუალო: {analytics.averagePrice.toFixed(0)}₾
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Charts Section */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Status Distribution */}
        <Card className="bg-gray-800 border-gray-700">
          <CardHeader>
            <CardTitle className="text-white flex items-center gap-2">
              <PieChart className="w-5 h-5 text-blue-400" />
              სტატუსების განაწილება
            </CardTitle>
            <CardDescription className="text-gray-400">
              მოთხოვნების მდგომარეობა
            </CardDescription>
          </CardHeader>
          <CardContent>
            <SimpleDonutChart data={statusData} />
          </CardContent>
        </Card>

        {/* Device Types */}
        <Card className="bg-gray-800 border-gray-700">
          <CardHeader>
            <CardTitle className="text-white flex items-center gap-2">
              <BarChart3 className="w-5 h-5 text-green-400" />
              მოწყობილობების ტიპები
            </CardTitle>
            <CardDescription className="text-gray-400">
              მომსახურების კატეგორიები
            </CardDescription>
          </CardHeader>
          <CardContent>
            <SimpleBarChart data={deviceData} />
          </CardContent>
        </Card>
      </div>

      {/* Additional Metrics */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Contact Messages */}
        <Card className="bg-gray-800 border-gray-700">
          <CardHeader>
            <CardTitle className="text-white flex items-center gap-2">
              <AlertCircle className="w-5 h-5 text-yellow-400" />
              კონტაქტების სტატისტიკა
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            <div className="flex justify-between">
              <span className="text-gray-300">სულ შეტყობინება:</span>
              <span className="text-white font-medium">{analytics.totalContacts}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-300">ახალი:</span>
              <Badge variant="secondary" className="bg-yellow-900 text-yellow-300">
                {contactMessages.filter(c => c.status === 'new').length}
              </Badge>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-300">წაკითხული:</span>
              <Badge variant="secondary" className="bg-blue-900 text-blue-300">
                {contactMessages.filter(c => c.status === 'read').length}
              </Badge>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-300">პასუხგაცემული:</span>
              <Badge variant="secondary" className="bg-green-900 text-green-300">
                {contactMessages.filter(c => c.status === 'replied').length}
              </Badge>
            </div>
          </CardContent>
        </Card>

        {/* Urgency Analysis */}
        <Card className="bg-gray-800 border-gray-700">
          <CardHeader>
            <CardTitle className="text-white flex items-center gap-2">
              <Clock className="w-5 h-5 text-red-400" />
              სისწრაფის ანალიზი
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            {Object.entries(analytics.urgencyCounts).map(([urgency, count]) => (
              <div key={urgency} className="flex justify-between items-center">
                <span className="text-gray-300 capitalize">{urgency}:</span>
                <Badge 
                  variant="secondary" 
                  className={`${
                    urgency === 'high' ? 'bg-red-900 text-red-300' :
                    urgency === 'medium' ? 'bg-yellow-900 text-yellow-300' :
                    'bg-green-900 text-green-300'
                  }`}
                >
                  {count}
                </Badge>
              </div>
            ))}
          </CardContent>
        </Card>

        {/* Performance Indicators */}
        <Card className="bg-gray-800 border-gray-700">
          <CardHeader>
            <CardTitle className="text-white flex items-center gap-2">
              <TrendingUp className="w-5 h-5 text-purple-400" />
              ეფექტურობის ინდიკატორები
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            <div className="space-y-2">
              <div className="flex justify-between">
                <span className="text-gray-300">დასრულების მაჩვენებელი:</span>
                <span className="text-green-400 font-medium">
                  {analytics.completionRate.toFixed(1)}%
                </span>
              </div>
              <div className="w-full bg-gray-700 rounded-full h-2">
                <div 
                  className="bg-green-500 h-2 rounded-full transition-all duration-300"
                  style={{ width: `${analytics.completionRate}%` }}
                />
              </div>
            </div>
            
            <div className="space-y-2">
              <div className="flex justify-between">
                <span className="text-gray-300">კმაყოფილების დონე:</span>
                <span className="text-yellow-400 font-medium">
                  {((analytics.averageRating / 5) * 100).toFixed(1)}%
                </span>
              </div>
              <div className="w-full bg-gray-700 rounded-full h-2">
                <div 
                  className="bg-yellow-500 h-2 rounded-full transition-all duration-300"
                  style={{ width: `${(analytics.averageRating / 5) * 100}%` }}
                />
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Export Button */}
      <div className="flex justify-end">
        <Button 
          variant="outline" 
          className="bg-gray-800 border-gray-700 text-white hover:bg-gray-700"
          onClick={() => {
            // Export functionality can be implemented here
            console.log('Export analytics data', analytics);
          }}
        >
          <Download className="w-4 h-4 mr-2" />
          Export Report
        </Button>
      </div>
    </div>
  );
};

export default AnalyticsDashboard;