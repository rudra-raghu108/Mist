import React, { useState, useEffect, useCallback } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { useToast } from '@/hooks/use-toast';
import type { Message } from "@/components/ChatMessage";
import { ChatInput } from './ChatInput';
import { QuickSuggestions } from './QuickSuggestions';
import { Sidebar } from './Sidebar';
import { ChatMessage } from './ChatMessage';
import { Menu, Sparkles, BookOpen, Users, GraduationCap } from 'lucide-react';
import { cn } from '@/lib/utils';
import { api } from '@/lib/api';

interface UserProfile {
  name: string;
  campus: string;
  focus: string;
}

export const MistAI: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isAutoScraping, setIsAutoScraping] = useState(true);
  const [isDark, setIsDark] = useState(false);
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [profile, setProfile] = useState<UserProfile>({
    name: '',
    campus: 'Any campus',
    focus: 'General'
  });
  
  const { toast } = useToast();

  // Theme management
  useEffect(() => {
    const savedTheme = localStorage.getItem('mist-ai-theme');
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    setIsDark(savedTheme === 'dark' || (!savedTheme && prefersDark));
  }, []);

  useEffect(() => {
    document.documentElement.classList.toggle('dark', isDark);
    localStorage.setItem('mist-ai-theme', isDark ? 'dark' : 'light');
  }, [isDark]);

  // Auto-scrape and train AI when component mounts
  useEffect(() => {
    const autoScrapeAndTrain = async () => {
      try {
        setIsAutoScraping(true);
        console.log('🚀 Auto-scraping SRM websites...');
        
        // Step 1: Start scraping
        const scrapingResponse = await api.scraping.start();
        console.log('Auto-scraping completed:', scrapingResponse);
        
        if (scrapingResponse.success) {
          // Step 2: Enhance AI knowledge with scraped data
          console.log('🧠 Enhancing AI knowledge with scraped data...');
          const enhancementResponse = await api.aiTraining.enhance();
          console.log('AI enhancement completed:', enhancementResponse);
          
          // Step 3: Load chat history
          console.log('📚 Loading chat history...');
          const historyResponse = await api.chat.getHistory('user_shadow');
          
          if (historyResponse.success && historyResponse.history) {
            const convertedMessages: Message[] = historyResponse.history.map((entry: any) => ({
              id: entry.timestamp.toString(),
              role: entry.type === 'user' ? 'user' : 'assistant',
              content: entry.message,
              timestamp: new Date(entry.timestamp * 1000), // Convert timestamp
            }));
            
            setMessages(convertedMessages);
            console.log('✅ Auto-setup completed: Scraping + AI Training + History Loaded');
          }
        }
      } catch (error) {
        console.error('Auto-setup failed:', error);
      } finally {
        setIsAutoScraping(false);
      }
    };

    autoScrapeAndTrain();
  }, []);

  // Real AI Response from Backend API with User Context
  const generateResponse = useCallback(async (query: string): Promise<string> => {
    try {
      console.log('Calling backend API for query:', query);
      console.log('API URL:', 'http://localhost:8000/api/chat');
      
      // Create a consistent user ID - use 'user_shadow' to match existing backend data
      const user_id = 'user_shadow'; // Fixed user ID to match backend
      console.log('Using user_id:', user_id);
      
      const response = await api.chat.send(query, user_id);
      console.log('Raw backend response:', response);
      console.log('Response type:', typeof response);
      console.log('Response keys:', Object.keys(response));
      
      if (response.error) {
        console.error('Backend returned error:', response);
        throw new Error(response.message || 'Failed to get AI response');
      }
      
      const aiResponse = response.response || response.message || 'Sorry, I couldn\'t process your request.';
      console.log('Extracted AI response:', aiResponse);
      
      return aiResponse;
    } catch (error) {
      console.error('AI API Error:', error);
      
      // Show the actual error in console
      if (error instanceof Error) {
        console.error('Error details:', error.message);
      }
      
      // Fallback to simple responses if API fails
      const lowerQuery = query.toLowerCase();
      
      if (lowerQuery.includes('hello') || lowerQuery.includes('hi') || lowerQuery.includes('hey')) {
        return 'Hello! I\'m your SRM Guide Bot. How can I help you today?';
      } else if (lowerQuery.includes('admission')) {
        return 'For SRM admissions, visit our website or contact the admissions office. Requirements include 10th & 12th marksheets and entrance exam scores.';
      } else if (lowerQuery.includes('courses')) {
        return 'SRM offers various courses including Engineering, Medicine, Management, and Arts. Popular ones are Computer Science, Electronics, and Mechanical Engineering.';
      } else if (lowerQuery.includes('hostel')) {
        return 'SRM provides hostel facilities with modern amenities. Fees range from ₹80,000 to ₹1,50,000 per year depending on room type.';
      } else {
        return 'I\'m here to help with SRM University information. You can ask about admissions, courses, hostel facilities, or any other queries.';
      }
    }
  }, []); // Removed profile dependency since we're using fixed user_id

  const handleSendMessage = async (content: string) => {
    if (!content.trim()) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: content.trim(),
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);

    try {
      console.log('Sending message to backend:', content);
      const response = await generateResponse(content);
      console.log('Backend response received:', response);
      console.log('Response length:', response.length);
      
      const botMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: response,
        timestamp: new Date(),
      };

      console.log('Creating bot message:', botMessage);
      setMessages(prev => [...prev, botMessage]);
      console.log('Message added to state');
    } catch (error) {
      console.error('Error in handleSendMessage:', error);
      toast({
        title: "Error",
        description: "Failed to get response from backend. Check console for details.",
        variant: "destructive",
      });
    } finally {
      setIsLoading(false);
      console.log('Loading state set to false');
    }
  };

  const handleSuggestionClick = (suggestion: string) => {
    handleSendMessage(suggestion);
  };

  const handleClearChat = () => {
    setMessages([]);
    toast({
      title: "Chat Cleared",
      description: "Your conversation history has been cleared.",
    });
  };

  const handleExportChat = () => {
    if (messages.length === 0) {
      toast({
        title: "No Messages",
        description: "There's no chat history to export.",
        variant: "destructive",
      });
      return;
    }

    const chatContent = messages.map(msg => 
      `${msg.role === 'user' ? 'You' : 'MIST AI'}: ${msg.content}\n\n`
    ).join('');

    const blob = new Blob([chatContent], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `mist-ai-chat-${new Date().toISOString().split('T')[0]}.txt`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);

    toast({
      title: "Chat Exported",
      description: "Your conversation has been downloaded as a text file.",
    });
  };

  const handleShowStats = () => {
    const userMessages = messages.filter(msg => msg.role === 'user').length;
    const botMessages = messages.filter(msg => msg.role === 'assistant').length;
    
    toast({
      title: "📊 Chat Statistics",
      description: `Total: ${messages.length} | You: ${userMessages} | AI: ${botMessages}`,
    });
  };

  const handleReset = () => {
    setMessages([]);
    setProfile({ name: '', campus: 'Any campus', focus: 'General' });
    localStorage.removeItem('mist-ai-profile');
    toast({
      title: "Reset Complete",
      description: "All settings and chat history have been reset.",
    });
  };

  const handleCopyMessage = (content: string) => {
    toast({
      title: "Copied!",
      description: "Message copied to clipboard.",
    });
    navigator.clipboard.writeText(content);
  };

  const handleProfileUpdate = (newProfile: Partial<UserProfile>) => {
    setProfile(prev => ({ ...prev, ...newProfile }));
    localStorage.setItem('mist-ai-profile', JSON.stringify({ ...profile, ...newProfile }));
    toast({
      title: "Profile Updated",
      description: "Your profile has been updated successfully.",
    });
  };

  // Load profile from localStorage
  useEffect(() => {
    const savedProfile = localStorage.getItem('mist-ai-profile');
    if (savedProfile) {
      try {
        setProfile(JSON.parse(savedProfile));
      } catch (error) {
        console.error('Error loading profile:', error);
      }
    }
  }, []);

  // Save profile to localStorage
  useEffect(() => {
    localStorage.setItem('mist-ai-profile', JSON.stringify(profile));
  }, [profile]);

  return (
    <div className="flex h-screen bg-gradient-hero">
              {/* Sidebar */}
        <Sidebar
          isOpen={sidebarOpen}
          onToggle={() => setSidebarOpen(!sidebarOpen)}
          isDark={isDark}
          onThemeToggle={() => setIsDark(!isDark)}
          profile={profile}
          onProfileUpdate={handleProfileUpdate}
          onClearChat={handleClearChat}
          onExportChat={handleExportChat}
          onShowStats={handleShowStats}
          onReset={handleReset}
          messageCount={messages.length}
        />

      {/* Main Content */}
      <div className="flex flex-1 flex-col">
        {/* Header */}
        <header className="border-b border-border bg-gradient-card/90 backdrop-blur-lg p-4 shadow-medium">
          <div className="flex items-center justify-between">
            {/* Menu button */}
            <Button
              variant="ghost"
              size="sm"
              onClick={() => setSidebarOpen(true)}
              className="md:hidden"
            >
              <Menu className="h-5 w-5" />
            </Button>

            <div className="flex items-center gap-4">
              <div className="flex items-center gap-3">
                <div className="h-10 w-10 rounded-full bg-gradient-header flex items-center justify-center shadow-glow">
                  <Sparkles className="h-5 w-5 text-white" />
                </div>
                <div>
                  <h1 className="text-xl font-bold bg-gradient-header bg-clip-text text-transparent">
                    ✨ MIST AI
                  </h1>
                  <p className="text-sm text-muted-foreground">SRM University Assistant</p>
                </div>
              </div>

              {/* Auto-scraping Status Indicator */}
              <div className="flex items-center gap-2 text-sm text-muted-foreground">
                {isAutoScraping ? (
                  <>
                    <div className="h-2 w-2 rounded-full bg-yellow-500 animate-pulse"></div>
                    <span>Deep scraping & training AI...</span>
                  </>
                ) : (
                  <>
                    <div className="h-2 w-2 rounded-full bg-green-500"></div>
                    <span>AI ready with comprehensive data</span>
                  </>
                )}
              </div>
            </div>

            <div className="flex items-center gap-2">
              <div className="hidden md:flex items-center gap-4 text-sm text-muted-foreground">
                {profile.name && <span>👤 {profile.name}</span>}
                {profile.campus !== 'Any campus' && <span>📍 {profile.campus}</span>}
                {profile.focus !== 'General' && <span>🎯 {profile.focus}</span>}
              </div>
            </div>
          </div>
        </header>

        {/* Chat Area */}
        <div className="flex-1 flex flex-col overflow-hidden">
          <div className="flex-1 overflow-y-auto p-4 space-y-6">
            {messages.length === 0 ? (
              <div className="mx-auto max-w-4xl">
                {/* Welcome Message */}
                <Card className="mb-8 border-0 shadow-strong bg-gradient-card overflow-hidden relative">
                  <div className="absolute inset-0 bg-gradient-header opacity-10"></div>
                  <CardContent className="p-12 text-center relative z-10">
                    <div className="mb-6">
                      <div className="mx-auto h-20 w-20 rounded-full bg-gradient-header flex items-center justify-center shadow-glow animate-pulse">
                        <Sparkles className="h-10 w-10 text-white" />
                      </div>
                    </div>
                    <h2 className="text-5xl font-extrabold mb-6 bg-gradient-header bg-clip-text text-transparent drop-shadow-lg tracking-tight">
                      ✨ MIST AI - SRM Assistant
                    </h2>
                    <p className="text-lg text-muted-foreground mb-8 font-medium">
                      {profile.name 
                        ? `👋 Hello ${profile.name}! I'm your friendly SRM guide for everything university-related` 
                        : "Your intelligent SRM University assistant for admissions, courses, campus life and more"}
                    </p>
                  </CardContent>
                </Card>

                {/* Quick Suggestions */}
                <QuickSuggestions onSuggestionClick={handleSuggestionClick} />
              </div>
            ) : (
              <div className="mx-auto max-w-4xl space-y-6">
                {messages.map((message) => (
                  <ChatMessage
                    key={message.id}
                    message={message}
                    onCopy={handleCopyMessage}
                  />
                ))}
                
                {isLoading && (
                  <div className="flex items-center gap-4 p-6 rounded-2xl bg-card shadow-soft border border-border">
                    <div className="flex h-10 w-10 items-center justify-center rounded-full bg-gradient-secondary text-secondary-foreground">
                      <Sparkles className="h-5 w-5" />
                    </div>
                    <div className="flex-1">
                      <div className="text-sm font-medium opacity-70 mb-2">MIST AI</div>
                      <div className="flex items-center gap-2 text-sm text-muted-foreground">
                        <Sparkles className="h-4 w-4 animate-pulse" />
                        <span>Thinking...</span>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            )}
          </div>

          {/* Chat Input */}
          <ChatInput onSend={handleSendMessage} disabled={isLoading} />
        </div>
      </div>
    </div>
  );
};