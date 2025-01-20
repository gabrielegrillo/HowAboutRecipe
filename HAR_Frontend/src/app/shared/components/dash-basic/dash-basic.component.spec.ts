import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DashBasicComponent } from './dash-basic.component';

describe('DashBasicComponent', () => {
  let component: DashBasicComponent;
  let fixture: ComponentFixture<DashBasicComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [DashBasicComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(DashBasicComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
