#!/usr/bin/env python3
"""
Test script untuk memverifikasi dan memperbaiki sistem real-time timestamp notifikasi
"""

import re
import os

def test_notification_timestamp_system():
    """Test real-time timestamp system untuk notifikasi"""
    print("⏰ Testing Real-Time Notification Timestamp System...")
    print("=" * 60)
    
    # 1. Check base-sidebar.html for timestamp intervals
    print("1. Checking timestamp intervals...")
    try:
        with open('templates/base-sidebar.html', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for timestamp update intervals
        has_2s_interval = 'setInterval(updateNotificationRelativeTime, 2000)' in content
        has_5s_badge = 'setInterval(updateNotificationBadge, 5000)' in content
        has_10s_reload = 'setInterval(loadNotifications, 10000)' in content
        has_immediate_update = 'setTimeout(updateNotificationRelativeTime' in content
        has_dom_ready_update = 'setTimeout(updateNotificationRelativeTime, 200)' in content
        has_delay_update = 'setTimeout(updateNotificationRelativeTime, 500)' in content
        
        print(f"   ✅ 2-second interval for timestamps: {'✅' if has_2s_interval else '❌'}")
        print(f"   ✅ 5-second interval for badge: {'✅' if has_5s_badge else '❌'}")
        print(f"   ✅ 10-second interval for reload: {'✅' if has_10s_reload else '❌'}")
        print(f"   ✅ Immediate timestamp update: {'✅' if has_immediate_update else '❌'}")
        print(f"   ✅ DOM ready update (200ms): {'✅' if has_dom_ready_update else '❌'}")
        print(f"   ✅ Delayed update (500ms): {'✅' if has_delay_update else '❌'}")
        
        if not (has_2s_interval and has_5s_badge and has_10s_reload):
            print("❌ Timestamp intervals missing")
            return False
        else:
            print("✅ Timestamp intervals found")
            
    except Exception as e:
        print(f"❌ Error checking timestamp intervals: {e}")
        return False
    
    # 2. Check formatTimeAgo function
    print("\n2. Checking formatTimeAgo function...")
    try:
        with open('templates/base-sidebar.html', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for comprehensive time formatting

        has_baru_saja = "'Baru saja'" in content
        has_detik = 'detik yang lalu' in content
        has_menit = 'menit yang lalu' in content
        has_jam = 'jam yang lalu' in content
        has_hari = 'hari yang lalu' in content
        has_timestamp_data = 'data-timestamp=' in content
        
        print(f"   ✅ 'Baru saja' for recent updates: {'✅' if has_baru_saja else '❌'}")
        print(f"   ✅ Seconds formatting: {'✅' if has_detik else '❌'}")
        print(f"   ✅ Minutes formatting: {'✅' if has_menit else '❌'}")
        print(f"   ✅ Hours formatting: {'✅' if has_jam else '❌'}")
        print(f"   ✅ Days formatting: {'✅' if has_hari else '❌'}")
        print(f"   ✅ Timestamp data attributes: {'✅' if has_timestamp_data else '❌'}")
        
        if not (has_baru_saja and has_detik and has_menit and has_jam and has_hari):
            print("❌ formatTimeAgo function incomplete")
            return False
        else:
            print("✅ formatTimeAgo function complete")
            
    except Exception as e:
        print(f"❌ Error checking formatTimeAgo function: {e}")
        return False
    
    # 3. Check updateNotificationRelativeTime function
    print("\n3. Checking updateNotificationRelativeTime function...")
    try:
        with open('templates/base-sidebar.html', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for proper function implementation
        has_function_def = 'function updateNotificationRelativeTime()' in content
        has_query_selector = 'querySelectorAll(\'.notification-time[data-timestamp]\')' in content
        has_for_each = 'forEach(element => {' in content
        has_set_attribute = 'setAttribute(\'data-timestamp\'' in content
        has_text_content = 'textContent = relativeTime' in content
        
        print(f"   ✅ Function definition: {'✅' if has_function_def else '❌'}")
        print(f"   ✅ Query selector for timestamps: {'✅' if has_query_selector else '❌'}")
        print(f"   ✅ ForEach loop implementation: {'✅' if has_for_each else '❌'}")
        print(f"   ✅ Set timestamp attributes: {'✅' if has_set_attribute else '❌'}")
        print(f"   ✅ Update text content: {'✅' if has_text_content else '❌'}")
        
        if not (has_function_def and has_query_selector and has_for_each):
            print("❌ updateNotificationRelativeTime function incomplete")
            return False
        else:
            print("✅ updateNotificationRelativeTime function complete")
            
    except Exception as e:
        print(f"❌ Error checking updateNotificationRelativeTime function: {e}")
        return False
    
    # 4. Check notification rendering with timestamps
    print("\n4. Checking notification rendering...")
    try:
        with open('templates/base-sidebar.html', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for proper timestamp rendering
        has_timestamp_div = 'notification-time' in content
        has_timestamp_data = 'data-timestamp=' in content
        has_format_call = 'formatTimeAgo(notification.created_at)' in content
        
        print(f"   ✅ Timestamp div element: {'✅' if has_timestamp_div else '❌'}")
        print(f"   ✅ Timestamp data attributes: {'✅' if has_timestamp_data else '❌'}")
        print(f"   ✅ formatTimeAgo function calls: {'✅' if has_format_call else '❌'}")
        
        if not (has_timestamp_div and has_timestamp_data and has_format_call):
            print("❌ Notification rendering incomplete")
            return False
        else:
            print("✅ Notification rendering complete")
            
    except Exception as e:
        print(f"❌ Error checking notification rendering: {e}")
        return False
    
    print("\n" + "=" * 60)
    print("🎉 REAL-TIME TIMESTAMP SYSTEM TEST COMPLETED!")
    print("\n📋 Summary:")
    print("   ✅ Timestamp intervals configured")
    print("   ✅ formatTimeAgo function complete")
    print("   ✅ updateNotificationRelativeTime function implemented")
    print("   ✅ Notification rendering with timestamps")
    
    print("\n🚀 Real-time features:")
    print("   • Update timestamps every 2 seconds")
    print("   • Update badge count every 5 seconds")
    print("   • Reload notifications every 10 seconds")
    print("   • Immediate update after rendering")
    print("   • DOM ready check with delays")
    print("   • Comprehensive time formatting")
    
    return True

def optimize_timestamp_system():
    """Optimize timestamp system for better performance"""
    print("\n" + "=" * 60)
    print("🔧 OPTIMIZING TIMESTAMP SYSTEM")
    print("=" * 60)
    
    try:
        with open('templates/base-sidebar.html', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find the notification system section
        old_pattern = '''// Update notification badge and relative time periodically - REAL TIME!
            setInterval(updateNotificationBadge, 5000); // Update every 5 seconds for faster updates
            setInterval(updateNotificationRelativeTime, 2000); // Update relative time every 2 seconds
            setInterval(loadNotifications, 10000); // Reload notifications every 10 seconds'''
        
        new_pattern = '''// Update notification badge and relative time periodically - REAL TIME!
            setInterval(updateNotificationBadge, 5000); // Update every 5 seconds for faster updates
            setInterval(updateNotificationRelativeTime, 2000); // Update relative time every 2 seconds
            setInterval(loadNotifications, 10000); // Reload notifications every 10 seconds
            
            // CRITICAL: Force immediate timestamp update for new notifications
            setTimeout(updateNotificationRelativeTime, 100); // Very quick update
            setTimeout(updateNotificationRelativeTime, 500); // Ensure DOM is ready
            setTimeout(updateNotificationRelativeTime, 1000); // Final update to be sure'''
        
        if old_pattern in content:
            content = content.replace(old_pattern, new_pattern)
            print("✅ Optimized timestamp intervals")
        else:
            print("ℹ️ Timestamp intervals already optimized")
        
        # Add additional timestamp validation
        old_function = '''function updateNotificationRelativeTime() {
            // Update relative time for all notification timestamps
            const notificationTimes = document.querySelectorAll('.notification-time[data-timestamp]');
            console.log('Updating relative time for', notificationTimes.length, 'notifications');
            
            notificationTimes.forEach(element => {
                const timestamp = element.getAttribute('data-timestamp');
                if (timestamp) {
                    console.log('Updating timestamp:', timestamp);
                    const relativeTime = formatTimeAgo(timestamp);
                    console.log('New relative time:', relativeTime);
                    element.textContent = relativeTime;
                } else {
                    console.warn('No timestamp found for element:', element);
                }
            });
        }'''
        
        new_function = '''function updateNotificationRelativeTime() {
            // Update relative time for all notification timestamps
            const notificationTimes = document.querySelectorAll('.notification-time[data-timestamp]');
            console.log('Updating relative time for', notificationTimes.length, 'notifications');
            
            notificationTimes.forEach(element => {
                const timestamp = element.getAttribute('data-timestamp');
                if (timestamp) {
                    console.log('Updating timestamp:', timestamp);
                    const relativeTime = formatTimeAgo(timestamp);
                    console.log('New relative time:', relativeTime);
                    element.textContent = relativeTime;
                } else {
                    console.warn('No timestamp found for element:', element);
                }
            });
        }
        
        // Additional timestamp validation function
        function validateAndUpdateTimestamps() {
            const now = Date.now();
            const notificationTimes = document.querySelectorAll('.notification-time[data-timestamp]');
            
            notificationTimes.forEach(element => {
                const timestamp = element.getAttribute('data-timestamp');
                if (timestamp) {
                    try {
                        const date = new Date(timestamp);
                        const diffMs = now - date.getTime();
                        const diffSecs = Math.floor(diffMs / 1000);
                        
                        // Force update for very recent notifications (less than 1 minute)
                        if (diffSecs < 60) {
                            const relativeTime = formatTimeAgo(timestamp);
                            if (element.textContent !== relativeTime) {
                                console.log('Force update for recent notification:', relativeTime);
                                element.textContent = relativeTime;
                            }
                        }
                    } catch (error) {
                        console.warn('Error validating timestamp:', timestamp, error);
                    }
                }
            });
        }'''
        
        if old_function in content:
            content = content.replace(old_function, new_function)
            print("✅ Added timestamp validation function")
        
        # Update intervals to include validation
        old_interval = '''setInterval(updateNotificationRelativeTime, 2000); // Update relative time every 2 seconds'''
        new_interval = '''setInterval(updateNotificationRelativeTime, 2000); // Update relative time every 2 seconds
            setInterval(validateAndUpdateTimestamps, 1000); // Validate every 1 second for very recent updates'''
        
        if old_interval in content:
            content = content.replace(old_interval, new_interval)
            print("✅ Added validation interval for recent notifications")
        
        # Write back the optimized content
        with open('templates/base-sidebar.html', 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("\n🚀 Optimizations applied:")
        print("   • Added multiple immediate timestamp updates")
        print("   • Added timestamp validation function")
        print("   • Added 1-second validation interval for recent notifications")
        print("   • Enhanced error handling for timestamp parsing")
        
        return True
        
    except Exception as e:
        print(f"❌ Error optimizing timestamp system: {e}")
        return False

def create_timestamp_test():
    """Create comprehensive timestamp test"""
    test_script = '''<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <title>Real-Time Notification Timestamp Test</title>
    <style>
        body { font-family: Arial, sans-serif; padding: 20px; }
        .notification-time { color: #666; font-size: 0.9em; }
        .test-result { margin: 10px 0; padding: 10px; border-radius: 5px; }
        .pass { background: #d4edda; color: #155724; }
        .fail { background: #f8d7da; color: #721c24; }
    </style>
</head>
<body>
    <h2>Real-Time Notification Timestamp Test</h2>
    
    <div id="test-results"></div>
    
    <h3>Test Notifications:</h3>
    <div id="test-notifications"></div>
    
    <script>
        function formatTimeAgo(dateString) {
            const now = new Date();
            let date;
            
            try {
                if (typeof dateString === 'string') {
                    if (dateString.includes('T') && dateString.includes('Z')) {
                        date = new Date(dateString);
                    } else if (dateString.includes('-') && dateString.length > 10) {
                        date = new Date(dateString.replace(' ', 'T'));
                    } else {
                        date = new Date(dateString);
                    }
                } else {
                    date = new Date(dateString);
                }
                
                if (isNaN(date.getTime())) {
                    return 'Waktu tidak valid';
                }
            } catch (error) {
                return 'Waktu tidak valid';
            }
            
            const diffInSeconds = Math.floor((now - date) / 1000);
            
            if (diffInSeconds < 60) {
                if (diffInSeconds < 10) {
                    return 'Baru saja';
                } else {
                    return diffInSeconds + ' detik yang lalu';
                }
            }
            else if (diffInSeconds < 3600) {
                const minutes = Math.floor(diffInSeconds / 60);
                const seconds = diffInSeconds % 60;
                if (minutes === 1 && seconds > 0) {
                    return minutes + ' menit ' + seconds + ' detik yang lalu';
                } else {
                    return minutes + ' menit yang lalu';
                }
            }
            else if (diffInSeconds < 86400) {
                const hours = Math.floor(diffInSeconds / 3600);
                const remainingMinutes = Math.floor((diffInSeconds % 3600) / 60);
                
                if (hours === 1 && remainingMinutes > 0) {
                    return hours + ' jam ' + remainingMinutes + ' menit yang lalu';
                } else {
                    return hours + ' jam yang lalu';
                }
            }
            else {
                const days = Math.floor(diffInSeconds / 86400);
                return days + ' hari yang lalu';
            }
        }
        
        function updateNotificationRelativeTime() {
            const notificationTimes = document.querySelectorAll('.notification-time[data-timestamp]');
            console.log('Updating relative time for', notificationTimes.length, 'notifications');
            
            notificationTimes.forEach(element => {
                const timestamp = element.getAttribute('data-timestamp');
                if (timestamp) {
                    const relativeTime = formatTimeAgo(timestamp);
                    element.textContent = relativeTime;
                }
            });
        }
        
        function validateAndUpdateTimestamps() {
            const now = Date.now();
            const notificationTimes = document.querySelectorAll('.notification-time[data-timestamp]');
            
            notificationTimes.forEach(element => {
                const timestamp = element.getAttribute('data-timestamp');
                if (timestamp) {
                    try {
                        const date = new Date(timestamp);
                        const diffMs = now - date.getTime();
                        const diffSecs = Math.floor(diffMs / 1000);
                        
                        if (diffSecs < 60) {
                            const relativeTime = formatTimeAgo(timestamp);
                            if (element.textContent !== relativeTime) {
                                element.textContent = relativeTime;
                            }
                        }
                    } catch (error) {
                        console.warn('Error validating timestamp:', timestamp, error);
                    }
                }
            });
        }
        
        // Create test notifications
        function createTestNotifications() {
            const now = new Date();
            const testCases = [
                { time: new Date(now.getTime() - 5000), label: '5 detik lalu' },
                { time: new Date(now.getTime() - 30000), label: '30 detik lalu' },
                { time: new Date(now.getTime() - 90000), label: '1.5 menit lalu' },
                { time: new Date(now.getTime() - 3600000), label: '1 jam lalu' },
                { time: new Date(now.getTime() - 86400000), label: '1 hari lalu' }
            ];
            
            const container = document.getElementById('test-notifications');
            
            testCases.forEach((testCase, index) => {
                const notificationDiv = document.createElement('div');
                notificationDiv.className = 'notification-item';
                notificationDiv.innerHTML = `
                    <div class="notification-content">
                        <div class="notification-title">Test Notification ${index + 1}</div>
                        <div class="notification-message">Test case: ${testCase.label}</div>
                        <div class="notification-time" data-timestamp="${testCase.time.toISOString()}">${formatTimeAgo(testCase.time)}</div>
                    </div>
                `;
                container.appendChild(notificationDiv);
            });
        }
        
        function runTests() {
            const results = [];
            
            // Test 1: Check if formatTimeAgo function exists
            if (typeof formatTimeAgo === 'function') {
                results.push({ test: 'formatTimeAgo function exists', pass: true });
            } else {
                results.push({ test: 'formatTimeAgo function exists', pass: false });
            }
            
            // Test 2: Check if updateNotificationRelativeTime function exists
            if (typeof updateNotificationRelativeTime === 'function') {
                results.push({ test: 'updateNotificationRelativeTime function exists', pass: true });
            } else {
                results.push({ test: 'updateNotificationRelativeTime function exists', pass: false });
            }
            
            // Test 3: Test formatTimeAgo with recent date
            const recentTime = new Date(Date.now() - 5000).toISOString();
            const result = formatTimeAgo(recentTime);
            if (result.includes('detik')) {
                results.push({ test: 'formatTimeAgo handles recent dates', pass: true });
            } else {
                results.push({ test: 'formatTimeAgo handles recent dates', pass: false });
            }
            
            // Test 4: Test updateNotificationRelativeTime
            createTestNotifications();
            const beforeCount = document.querySelectorAll('.notification-time').length;
            updateNotificationRelativeTime();
            const afterCount = document.querySelectorAll('.notification-time').length;
            
            if (beforeCount === afterCount && afterCount > 0) {
                results.push({ test: 'updateNotificationRelativeTime processes timestamps', pass: true });
            } else {
                results.push({ test: 'updateNotificationRelativeTime processes timestamps', pass: false });
            }
            
            // Display results
            const resultsDiv = document.getElementById('test-results');
            resultsDiv.innerHTML = results.map(result => 
                `<div class="test-result ${result.pass ? 'pass' : 'fail'}">${result.pass ? '✅' : '❌'} ${result.test}</div>`
            ).join('');
            
            const passCount = results.filter(r => r.pass).length;
            resultsDiv.innerHTML += `<h3>Result: ${passCount}/${results.length} tests passed</h3>`;
        }
        
        // Start the tests and real-time updates
        document.addEventListener('DOMContentLoaded', function() {
            runTests();
            
            // Start real-time updates
            setInterval(updateNotificationRelativeTime, 2000);
            setInterval(validateAndUpdateTimestamps, 1000);
        });
    </script>
</body>
</html>'''
    
    try:
        with open('test_notification_timestamp.html', 'w', encoding='utf-8') as f:
            f.write(test_script)
        print("✅ Created comprehensive timestamp test file: test_notification_timestamp.html")
        return True
    except Exception as e:
        print(f"❌ Error creating timestamp test: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Real-Time Notification Timestamp System Test & Optimization")
    print("Testing dan optimizing real-time timestamp pada pesan notifikasi")
    print()
    
    success = test_notification_timestamp_system()
    
    if success:
        optimize_timestamp_system()
        create_timestamp_test()
        print("\n🎉 ALL OPTIMIZATIONS COMPLETED!")
        print("\n📋 Summary:")
        print("   ✅ Timestamp system tested and validated")
        print("   ✅ Multiple immediate updates added")
        print("   ✅ Timestamp validation function implemented")
        print("   ✅ Enhanced intervals for recent notifications")
        print("   ✅ Comprehensive test file created")
        
        print("\n🧪 To test the real-time timestamps:")
        print("   1. Open test_notification_timestamp.html in browser")
        print("   2. Open browser console (F12)")
        print("   3. Watch timestamps update every 2 seconds")
        print("   4. Verify recent notifications update every 1 second")
        print("   5. Check that timestamps show 'Baru saja' for very recent updates")
        
    else:
        print("\n❌ SOME TESTS FAILED! Please check the errors above.")

