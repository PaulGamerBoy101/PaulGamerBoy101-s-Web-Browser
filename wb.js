import React, { useState, useRef } from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Tab, Tabs, TabList, TabPanel } from 'react-tabs';
import 'react-tabs/style/react-tabs.css';

const Browser = () => {
  const [tabs, setTabs] = useState(["https://custom-new-tab-page-12935782.codehs.me/"]);
  const [activeTab, setActiveTab] = useState(0);
  const browserRefs = useRef([]);

  const handleNavigation = (action, tabIndex) => {
    const browser = browserRefs.current[tabIndex];
    if (!browser) return;

    switch (action) {
      case 'back':
        browser.history.back();
        break;
      case 'forward':
        browser.history.forward();
        break;
      case 'reload':
        browser.src = browser.src;
        break;
      case 'home':
        updateTab(tabIndex, "https://custom-new-tab-page-12935782.codehs.me/");
        break;
      default:
        break;
    }
  };

  const updateTab = (tabIndex, url) => {
    const updatedTabs = [...tabs];
    updatedTabs[tabIndex] = url;
    setTabs(updatedTabs);
  };

  const handleSearch = (tabIndex, url) => {
    if (!url.startsWith('http')) {
      url = `https://${url}`;
    }
    updateTab(tabIndex, url);
  };

  const addNewTab = () => {
    setTabs([...tabs, "https://custom-new-tab-page-12935782.codehs.me/"]);
    setActiveTab(tabs.length);
  };

  const closeTab = (index) => {
    if (tabs.length === 1) return;
    const newTabs = tabs.filter((_, i) => i !== index);
    setTabs(newTabs);
    setActiveTab(Math.max(0, activeTab - 1));
  };

  return (
    <Card className="w-full h-screen flex flex-col">
      <CardContent className="p-2 bg-gray-100 border-b flex flex-col">
        <Tabs
          selectedIndex={activeTab}
          onSelect={(index) => setActiveTab(index)}
          selectedTabClassName="bg-white shadow">
          <TabList className="flex gap-2">
            {tabs.map((tab, index) => (
              <Tab
                key={index}
                className="p-2 bg-gray-200 rounded flex items-center gap-2">
                <span>Tab {index + 1}</span>
                <Button
                  variant="ghost"
                  onClick={(e) => {
                    e.stopPropagation();
                    closeTab(index);
                  }}>
                  ✖
                </Button>
              </Tab>
            ))}
            <Button onClick={addNewTab} variant="outline">
                
