
#ifndef VEC3_H
#define VEC3_H
class Vec3
{
  public :
    Vec3()=default;
    ~Vec3() noexcept =default;
    Vec3(const Vec3 &)=default;
    Vec3 & operator=(const Vec3 &)=default;
    Vec3(Vec3 &&)=default;
    Vec3 & operator=(Vec3 &&)=default;
};

#endif
