/**
 * Home Page - Presentation Layer
 */
import React from 'react';
import { TextGenerator } from '../components/TextGenerator';
import { getDIContainer } from '../../application/diContainer';
import '../styles/Home.css';

export const HomePage: React.FC = () => {
  const diContainer = getDIContainer();
  const generateUseCase = diContainer.getGenerateTextUseCase();

  return (
    <div className="home-page">
      <header className="header">
        <h1>Simple GPT</h1>
        <p>A lightweight NLP text generation service</p>
      </header>

      <main className="main-content">
        <TextGenerator
          useCase={generateUseCase}
          onPredictionGenerated={(id) => {
            console.log('Prediction generated:', id);
          }}
        />
      </main>

      <footer className="footer">
        <p>&copy; 2026 Simple GPT. Built with Python + TypeScript</p>
      </footer>
    </div>
  );
};
