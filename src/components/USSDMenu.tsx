import React, { useState } from 'react';
import { Text, Button } from '@mantine/core';
type MenuLevel = 'main' | 'sell' | 'prices' | 'wallet' | 'confirm';
export function USSDMenu() {
  const [menu, setMenu] = useState<MenuLevel>('main');
  const [response, setResponse] = useState<string>('');
  const [history, setHistory] = useState<MenuLevel[]>(['main']);
  const handleOption = (option: string) => {
    switch (menu) {
      case 'main':
        switch (option) {
          case '1':
            setMenu('sell');
            setHistory([...history, 'sell']);
            break;
          case '2':
            setMenu('prices');
            setHistory([...history, 'prices']);
            break;
          case '3':
            setMenu('wallet');
            setHistory([...history, 'wallet']);
            break;
        }
        break;
      case 'sell':
        if (option === '1') {
          setMenu('confirm');
          setHistory([...history, 'confirm']);
        } else {
          setMenu('main');
          setHistory(['main']);
        }
        break;
      case 'confirm':
        setMenu('main');
        setHistory(['main']);
        setResponse(option === '1' ? 'Sale confirmed! You will receive 50 KES/kg via M-PESA shortly.' : 'Sale cancelled.');
        setTimeout(() => setResponse(''), 3000);
        break;
      default:
        setMenu('main');
        setHistory(['main']);
    }
  };
  const handleBack = () => {
    if (history.length > 1) {
      const newHistory = [...history];
      newHistory.pop();
      setHistory(newHistory);
      setMenu(newHistory[newHistory.length - 1]);
    }
  };
  const renderMenu = () => {
    switch (menu) {
      case 'main':
        return <>
            <MenuTitle text="MAIN MENU" />
            <MenuOption num="1" text="SELL CROPS" />
            <MenuOption num="2" text="CHECK PRICES" />
            <MenuOption num="3" text="MY WALLET" />
            <MenuOption num="0" text="EXIT" />
          </>;
      case 'sell':
        return <>
            <MenuTitle text="SELL CROPS" />
            <Text className="mb-4 text-xs">Current maize price: 50 KES/kg</Text>
            <MenuOption num="1" text="SELL NOW" />
            <MenuOption num="2" text="CHECK OTHER BUYERS" />
            <MenuOption num="0" text="BACK" />
          </>;
      case 'prices':
        return <>
            <MenuTitle text="MARKET PRICES" />
            <Text className="mb-2 text-xs">NAIROBI PRICES (KES/KG):</Text>
            <Text className="text-xs">MAIZE: 50</Text>
            <Text className="text-xs">BEANS: 120</Text>
            <Text className="text-xs">POTATOES: 45</Text>
            <Text className="text-xs mb-4">ONIONS: 60</Text>
            <MenuOption num="0" text="BACK" />
          </>;
      case 'wallet':
        return <>
            <MenuTitle text="MY WALLET" />
            <Text className="mb-2 text-xs">BALANCE:</Text>
            <Text className="text-xs">USDC: $45.75</Text>
            <Text className="text-xs mb-4">M-PESA: KES 5,230</Text>
            <MenuOption num="0" text="BACK" />
          </>;
      case 'confirm':
        return <>
            <MenuTitle text="CONFIRM SALE" />
            <Text className="mb-4 text-xs">
              Sell 100kg maize at 50 KES/kg? Total: KES 5,000
            </Text>
            <MenuOption num="1" text="CONFIRM" />
            <MenuOption num="2" text="CANCEL" />
          </>;
    }
  };
  return <div className="space-y-4">
      {response ? <Text className="text-xs text-center p-4">{response}</Text> : renderMenu()}
      <div className="flex justify-between mt-4 pt-4 border-t border-green-500">
        {history.length > 1 && <Button variant="outline" color="green" size="xs" onClick={handleBack} className="flex-1 mr-2">
            BACK
          </Button>}
        <Button variant="outline" color="green" size="xs" onClick={() => setMenu('main')} className="flex-1">
          MAIN MENU
        </Button>
      </div>
      <div className="text-xs text-center mt-4">
        Enter number and press send
      </div>
      <div className="grid grid-cols-3 gap-2 text-black">
  {['1', '2', '3', '4', '5', '6', '7', '8', '9', '*', '0', '#'].map(num => (
    <Button 
      key={num} 
      variant="outline" 
      color="green" 
      size="xs" 
      onClick={() => handleOption(num)} 
      className={`aspect-square ${['1', '2', '3','4', '5', '6', '7', '8', '9', '*', '0', '#'].includes(num) ? 'text-black' : ''}`}
    >
      {num}
    </Button>
  ))}
</div>
    </div>;
}
function MenuTitle({
  text
}: {
  text: string;
}) {
  return <Text className="text-center font-bold mb-4 border-b border-green-500 pb-2">
      {text}
    </Text>;
}
function MenuOption({
  num,
  text
}: {
  num: string;
  text: string;
}) {
  return <Text className="text-xs mb-2">
      {num}. {text}
    </Text>;
}