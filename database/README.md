# UFC Database Solution

A comprehensive SQLite database solution for the UFC data project, designed to support prediction modeling and DraftKings fantasy lineup generation.

## 🏗️ Architecture Overview

The database solution consists of several key components:

- **Database Schema** (`database_schema.py`) - Core database structure and table definitions
- **Data Access Layer** (`data_access_layer.py`) - High-level CRUD operations and data management
- **Data Migration** (`data_migration.py`) - Scripts to import existing CSV data
- **Database Utilities** (`database_utils.py`) - Analytics, reporting, and query builders
- **Configuration** (`config.py`) - Database configuration and settings

## 📊 Database Schema

### Core Tables

#### Fighters
- `fighter_id` (Primary Key)
- `name` (Unique)
- `height`, `reach`, `stance`
- `date_of_birth`
- Timestamps

#### Events
- `event_id` (Primary Key)
- `name`, `date`
- `location`, `venue`
- Timestamps

#### Weight Classes
- `weight_class_id` (Primary Key)
- `name` (Unique)
- `weight_limit`, `gender`
- Timestamps

#### Fights
- `fight_id` (Primary Key)
- Foreign keys to `events`, `fighters`, `weight_classes`
- `outcome`, `method`, `round`, `time`
- `referee`
- Timestamps

#### Fighter Stats
- Historical fighter statistics at time of each fight
- Performance metrics (strikes, takedowns, submissions)
- Win/loss records
- Linked to specific fights

#### Betting Odds
- `odds_id` (Primary Key)
- Foreign keys to `fights` and `fighters`
- `favourite_odds`, `underdog_odds`
- `betting_outcome`
- `bookmaker`, `odds_date`

### Prediction & Analytics Tables

#### Prediction Models
- `model_id` (Primary Key)
- Model metadata (name, type, version)
- Performance metrics (accuracy, precision, recall, F1)
- Training information
- Model file paths

#### Predictions
- `prediction_id` (Primary Key)
- Foreign keys to `models` and `fights`
- Prediction results and confidence scores
- Feature values used
- Actual outcomes for validation

### DraftKings Integration Tables

#### DraftKings Lineups
- `lineup_id` (Primary Key)
- Foreign key to `events`
- Lineup metadata (name, salary, projected points)

#### DraftKings Lineup Fighters
- Composition of each lineup
- Fighter salaries and projected points
- Actual performance tracking

## 🚀 Quick Start

### 1. Initialize Database

```python
from database_schema import UFCDatabase

# Create database and tables
db = UFCDatabase("ufc_data.db")
db.create_tables()
db.create_indexes()
db.close()
```

### 2. Migrate Existing Data

```python
from data_migration import UFCDataMigrator

# Migrate CSV data to database
migrator = UFCDataMigrator("ufc_data.db", ".")
migrator.migrate_complete_data("complete_ufc_data.csv")
migrator.close()
```

### 3. Basic Data Operations

```python
from data_access_layer import UFCDataAccess

dal = UFCDataAccess("ufc_data.db")

# Insert a new fighter
fighter_id = dal.insert_fighter("New Fighter", height=72.0, reach=74.0)

# Get fighter information
fighter = dal.get_fighter_by_id(fighter_id)

# Get recent fights
recent_fights = dal.get_recent_fights(fighter_id, limit=5)

dal.close()
```

## 📈 Analytics and Reporting

### Fighter Performance Analysis

```python
from database_utils import UFCQueryBuilder, UFCAnalytics
from data_access_layer import UFCDataAccess

dal = UFCDataAccess("ufc_data.db")
analytics = UFCAnalytics(dal)
query_builder = UFCQueryBuilder(dal)

# Get fighter performance metrics
fighter_id = dal.get_fighter_id_by_name("Conor McGregor")
metrics = query_builder.get_fighter_performance_metrics(fighter_id)

# Head-to-head comparison
fighter2_id = dal.get_fighter_id_by_name("Nate Diaz")
comparison = query_builder.get_head_to_head_comparison(fighter_id, fighter2_id)

# Fighter rankings
rankings = analytics.get_fighter_rankings(limit=20)

dal.close()
```

### Event Analysis

```python
# Generate event report
event_id = dal.get_event_id_by_name_and_date("UFC 300", "2024-04-13")
report = analytics.generate_event_report(event_id)

# Betting analysis for a fight
fight_id = 12345
betting_analysis = query_builder.get_betting_analysis(fight_id)
```

## 🤖 Prediction Model Integration

### Storing Model Information

```python
# Register a new prediction model
model_id = dal.insert_prediction_model(
    model_name="GBM_v1",
    model_type="GradientBoosting",
    version="1.0",
    accuracy=0.67,
    features_used=["delta_strikes_pm", "delta_win_pct", "odds_ratio"],
    hyperparameters={"n_estimators": 100, "learning_rate": 0.1},
    model_file_path="/models/gbm_v1.pkl",
    is_active=True
)
```

### Making Predictions

```python
# Store a prediction
prediction_id = dal.insert_prediction(
    model_id=model_id,
    fight_id=fight_id,
    predicted_winner_id=fighter1_id,
    confidence_score=0.73,
    prediction_probabilities={"fighter1": 0.73, "fighter2": 0.27},
    features_used={"delta_strikes_pm": 1.2, "delta_win_pct": 0.15}
)

# Update with actual outcome
dal.update_prediction_outcome(prediction_id, "fighter1", True)
```

### Feature Extraction

```python
# Extract features for prediction
features = query_builder.get_prediction_features_for_fight(fight_id)
```

## 🎯 DraftKings Integration

### Creating Lineups

```python
# Create a new lineup
lineup_id = dal.insert_draftkings_lineup(
    event_id=event_id,
    lineup_name="High Upside Lineup",
    total_salary=50000,
    projected_points=85.5
)

# Add fighters to lineup
dal.insert_lineup_fighter(
    lineup_id=lineup_id,
    fighter_id=fighter_id,
    salary=8500,
    projected_points=12.3,
    position="Fighter"
)

# Get complete lineup
lineup = dal.get_lineup_with_fighters(lineup_id)
```

## 🔧 Database Utilities

### Data Export

```python
from database_utils import export_to_csv, backup_database

# Export table to CSV
export_to_csv(dal, "fighters", "fighters_export.csv")

# Export custom query
query = """
SELECT f.name, COUNT(*) as fights, 
       AVG(CASE WHEN outcome = 'fighter1' THEN 1 ELSE 0 END) as win_rate
FROM fighters f
JOIN fights ON f.fighter_id = fights.fighter1_id
GROUP BY f.fighter_id, f.name
HAVING fights >= 5
ORDER BY win_rate DESC
"""
export_to_csv(dal, None, "fighter_stats.csv", query)

# Backup database
backup_database("ufc_data.db", "backup_ufc_data.db")
```

### Performance Monitoring

```python
# Get model performance report
model_performance = analytics.get_model_performance_report(model_id)

# Weight class statistics
weight_class_id = dal.get_weight_class_id_by_name("Lightweight")
stats = query_builder.get_weight_class_statistics(weight_class_id)
```

## 📋 Database Indexes

The database includes optimized indexes for:

- Fighter name lookups
- Event date queries
- Fight outcome analysis
- Betting odds retrieval
- Prediction model performance
- DraftKings lineup optimization

## 🔒 Data Integrity

### Foreign Key Constraints
- All relationships enforced with foreign keys
- Cascade deletes where appropriate
- Referential integrity maintained

### Data Validation
- Check constraints on enum fields
- Required field validation
- Unique constraints on business keys

### Timestamps
- Automatic creation and update timestamps
- Data lineage tracking
- Extract timestamp preservation

## 🚀 Performance Optimization

### Indexing Strategy
- Primary keys automatically indexed
- Foreign keys indexed for join performance
- Composite indexes on frequently queried combinations
- Covering indexes for common SELECT patterns

### Query Optimization
- Use prepared statements for repeated queries
- Leverage SQLite query planner
- Monitor query execution plans
- Batch operations for bulk inserts

### Memory Management
- Connection pooling for concurrent access
- Proper transaction management
- Regular VACUUM operations for space reclamation

## 🔄 Maintenance

### Regular Tasks
- Database backup (daily recommended)
- Index maintenance and statistics updates
- Data validation checks
- Performance monitoring

### Data Updates
- Incremental updates for new events
- Fighter statistics refresh
- Odds data synchronization
- Model retraining triggers

## 🐛 Troubleshooting

### Common Issues

1. **Foreign Key Violations**
   - Ensure referenced records exist before insertion
   - Check data migration order

2. **Performance Issues**
   - Analyze query execution plans
   - Consider additional indexes
   - Review transaction boundaries

3. **Data Inconsistencies**
   - Run data validation queries
   - Check migration logs
   - Verify source data quality

### Logging
- All operations logged with timestamps
- Error tracking and reporting
- Performance metrics collection

## 📚 API Reference

See individual module documentation:
- `database_schema.py` - Core database operations
- `data_access_layer.py` - High-level data management
- `database_utils.py` - Analytics and utilities
- `data_migration.py` - Data import and migration

## 🤝 Contributing

When extending the database:
1. Follow the established naming conventions
2. Add appropriate indexes for new queries
3. Include data validation
4. Update documentation
5. Add unit tests for new functionality

## 📄 License

This database solution is part of the UFC data project and follows the same licensing terms.
