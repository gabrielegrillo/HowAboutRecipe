import { Routes } from '@angular/router';

import { LoginComponent } from './business/login/login.component';
import { RecipeComponent } from './business/recipe/recipe.component';
import { HomeComponent } from './business/home/home.component';
import { DashBasicComponent } from './shared/components/dash-basic/dash-basic.component';
import { DashRecipesComponent } from './shared/components/dash-recipes/dash-recipes.component';

import { authGuard } from './shared/utils/auth.guard';

export const routes: Routes = [
  { 
    path: '', 
    redirectTo: 'home',
    pathMatch: 'full' 
  },
  { 
    path: 'home', 
    loadComponent: () => import('./business/home/home.component').then((c) => c.HomeComponent )
  },
  { 
    path: 'login', 
    loadComponent: () => import('./business/login/login.component').then((c) => c.LoginComponent ) 
  },
  {
    path: 'recipes/:recipeId',
    loadComponent: () => import('./business/recipe/recipe.component').then((c) => c.RecipeComponent),
  },

  // { 
  //   path: 'dashboard', 
  //   loadComponent: () => import('./business/dashboard/dashboard.component').then((c) => c.DashboardComponent ) ,
  //   children: [
  //     {
  //       path: '', 
  //       component: DashBasicComponent
  //     },
  //     {
  //       path: '/recipes',
  //       component: DashRecipesComponent
  //     }
  //   ],
  //   canActivate: [authGuard]
  // },


  /* Lazy Loading -> loadComponent: () => import('./business/home/home.component').then((c) => c.HomeComponent ) */
  /* ---- Not Found Page ---- */
  {
    path: '**',
    loadComponent: () => import('./business/not-found-page/not-found-page.component').then((c) => c.NotFoundPageComponent),
  }
];
