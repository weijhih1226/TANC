program read_qpesums_grid

implicit none

integer   :: ii,jj,zz
character :: filename*256
integer   :: yyyy,mm,dd,hh,mn,ss,nx,ny,nz  ! 1-9th vars
character :: proj*4                        ! 10th vars
integer   :: map_scale,projlat1,projlat2,projlon,alon,alat,xy_scale,dx,dy,dxy_scale ! 11-20th vars
integer   :: z_scale,i_bb_mode,unkn01(9)
character :: varname*20,varunit*6
integer   :: var_scale,missing,nradar
integer,allocatable   :: zht(:)
character,allocatable :: mosradar(:,:)
integer*2,allocatable :: var(:,:)

call getarg(1,filename)

open(11,file=trim(filename),form='unformatted',status='old',access='stream')
!open(11,file=trim(filename),form='binary',status='old')
read(11) yyyy,mm,dd,hh,mn,ss,nx,ny,nz,proj,&
         map_scale,projlat1,projlat2,projlon,alon,alat,&
         xy_scale,dx,dy,dxy_scale
allocate(var(nx,ny),zht(nz))
read(11) zht,z_scale,i_bb_mode,unkn01,varname,varunit,&
         var_scale,missing,nradar
allocate(mosradar(4,nradar))
read(11) mosradar,var
close(11)

write(*,*) 'yyyy  = ',yyyy
write(*,*) 'mm    = ',mm
write(*,*) 'dd    = ',dd
write(*,*) 'hh    = ',hh
write(*,*) 'mn    = ',mn
write(*,*) 'ss    = ',ss
write(*,*) 'nx    = ',nx
write(*,*) 'ny    = ',ny
write(*,*) 'nz    = ',nz
write(*,*) 'proj  = ',proj
write(*,*) 'map_scale  = ',map_scale
write(*,*) 'projlat1   = ',projlat1
write(*,*) 'projlat2   = ',projlat2
write(*,*) 'projlon    = ',projlon
write(*,*) 'alon       = ',alon
write(*,*) 'alat       = ',alat
write(*,*) 'xy_scale   = ',xy_scale
write(*,*) 'dx         = ',dx
write(*,*) 'dy         = ',dy
write(*,*) 'dxy_scale  = ',dxy_scale
write(*,*) 'zht        = '
do ii = 1,nz
  write(*,*) '             ',zht(ii)
end do
write(*,*) 'z_scale    = ',z_scale
write(*,*) 'i_bb_mode  = ',i_bb_mode
write(*,*) 'unkn01     = ',unkn01
write(*,*) 'varname    = ',varname
write(*,*) 'varunit    = ',varunit
write(*,*) 'var_scale  = ',var_scale
write(*,*) 'missing    = ',missing
write(*,*) 'nradar     = ',nradar
  write(*,*) 'mosradar   = '
do ii = 1,nradar
  write(*,*) '             ',mosradar(:,ii)
end do
write(*,*) minval(var),maxval(var)
write(*,*) minval(var,var.gt.-999*var_scale),maxval(var)
write(*,*) minval(var,var.gt. -99*var_scale),maxval(var)

!do zz = 1,ny
!do ii = 1,nx
!  write(*,*) var(ii,zz)
!end do
!end do

deallocate(var,zht,mosradar)

end
