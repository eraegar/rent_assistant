/**
 * Утилиты для форматирования номеров телефонов
 */

/**
 * Форматирует номер телефона в российский формат +7 (XXX) XXX-XX-XX
 * @param value - введенный номер телефона
 * @returns отформатированный номер
 */
export const formatPhoneNumber = (value: string): string => {
  // Удаляем все нечисловые символы кроме +
  const numbers = value.replace(/[^\d+]/g, '');
  
  // Если пустая строка
  if (!numbers) return '';
  
  // Если начинается с 8, заменяем на +7
  let cleanNumbers = numbers;
  if (cleanNumbers.startsWith('8')) {
    cleanNumbers = '+7' + cleanNumbers.slice(1);
  }
  
  // Если не начинается с +7, добавляем +7
  if (!cleanNumbers.startsWith('+7')) {
    if (cleanNumbers.startsWith('+')) {
      cleanNumbers = '+7' + cleanNumbers.slice(1);
    } else {
      cleanNumbers = '+7' + cleanNumbers;
    }
  }
  
  // Удаляем лишние символы после +7
  const digits = cleanNumbers.slice(2); // убираем +7
  
  // Ограничиваем до 10 цифр после +7
  const limitedDigits = digits.slice(0, 10);
  
  // Форматируем в зависимости от количества введенных цифр
  if (limitedDigits.length === 0) {
    return '+7';
  } else if (limitedDigits.length <= 3) {
    return `+7 (${limitedDigits}`;
  } else if (limitedDigits.length <= 6) {
    return `+7 (${limitedDigits.slice(0, 3)}) ${limitedDigits.slice(3)}`;
  } else {
    const part1 = limitedDigits.slice(0, 3);
    const part2 = limitedDigits.slice(3, 6);
    const part3 = limitedDigits.slice(6, 8);
    const part4 = limitedDigits.slice(8, 10);
    
    let formatted = `+7 (${part1}) ${part2}`;
    if (part3) {
      formatted += `-${part3}`;
    }
    if (part4) {
      formatted += `-${part4}`;
    }
    
    return formatted;
  }
};

/**
 * Извлекает чистый номер телефона из отформатированной строки
 * @param formattedPhone - отформатированный номер
 * @returns чистый номер в формате +7XXXXXXXXXX
 */
export const getCleanPhoneNumber = (formattedPhone: string): string => {
  const numbers = formattedPhone.replace(/[^\d+]/g, '');
  
  if (numbers.startsWith('8')) {
    return '+7' + numbers.slice(1);
  }
  
  if (!numbers.startsWith('+7')) {
    if (numbers.startsWith('+')) {
      return '+7' + numbers.slice(1);
    } else {
      return '+7' + numbers;
    }
  }
  
  return numbers;
};

/**
 * Проверяет, является ли номер телефона валидным
 * @param phone - номер телефона
 * @returns true если номер валидный
 */
export const isValidPhoneNumber = (phone: string): boolean => {
  const cleanPhone = getCleanPhoneNumber(phone);
  // Проверяем что номер начинается с +7 и содержит 11 цифр (включая 7)
  return /^\+7\d{10}$/.test(cleanPhone);
};

/**
 * Хук для форматирования номера телефона в поле ввода
 * @param initialValue - начальное значение
 * @returns объект с форматированным значением и функцией обновления
 */
export const usePhoneFormatter = (initialValue = '') => {
  const formatAndUpdate = (value: string): string => {
    return formatPhoneNumber(value);
  };
  
  const getCleanValue = (formattedValue: string): string => {
    return getCleanPhoneNumber(formattedValue);
  };
  
  return {
    formatAndUpdate,
    getCleanValue,
    isValid: (value: string) => isValidPhoneNumber(value)
  };
}; 