using FireSprinkler.Api.Models; using Microsoft.EntityFrameworkCore;
namespace FireSprinkler.Api.Data;
public sealed class AppDbContext(DbContextOptions<AppDbContext> options):DbContext(options) { public DbSet<MonitoringPoint> Points=>Set<MonitoringPoint>(); public DbSet<MonitoringEvent> Events=>Set<MonitoringEvent>(); protected override void OnModelCreating(ModelBuilder b){ b.Entity<MonitoringPoint>().HasKey(x=>x.PointId); b.Entity<MonitoringEvent>().HasIndex(x=>x.EventId).IsUnique(); b.Entity<MonitoringEvent>().HasIndex(x=>new{x.PointId,x.OccurredAt}); } }
