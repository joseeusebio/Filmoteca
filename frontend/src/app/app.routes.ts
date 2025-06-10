import { Routes } from '@angular/router';
import { Home } from './home/home';
import { MovieDetail } from './pages/movie-detail/movie-detail';

export const appRoutes: Routes = [
  {
    path: '',
    component: Home
  },
  {
    path: 'movie/:id',
    component: MovieDetail
  },
  {
    path: '**',
    redirectTo: ''
  }
];
