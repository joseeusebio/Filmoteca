import { Routes } from '@angular/router';
import { Home } from './home/home';

export const appRoutes: Routes = [
  {
    path: '',
    component: Home
  },
  {
    path: '**',
    redirectTo: ''
  }
];
